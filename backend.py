#!/usr/bin/env python3

import argparse
import json
import logging
import os
import pathlib
import datetime
import socket
import sys

import asyncio
import graphviz
from aiohttp import web

from labgrid.remote.client import ClientSession, start_session
from labgrid.remote.common import Place
from labgrid.resource import Resource

data = {}
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter("%(asctime)s:\t %(message)s")
for h in logger.handlers:
    logger.removeHandler(h)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

CONFIGS_DIR = pathlib.Path("/usr/share/labgrid/configs")
session = None


async def do_graph(session: ClientSession) -> bytes:
    # Was copied from contrib/labgrid-webapp
    '''Generate a graphviz graph of the current configuration.

    Graph displays:
    - all resources, grouped by groupname and exporter.
    - all places, with a list of tags
    - solid edges between places and acquired resources
    - dotted edges between places and unacquired resources
    - edges between resources and places carry the match name if any.
    '''
    def res_node_attr(name: str, resource: Resource) -> dict[str, str]:
        return {
            'shape': 'plaintext',
            'label': f'''<
            <table bgcolor="peru">
                <tr>
                    <td border="0" align="left">Resource</td>
                </tr>
                <tr>
                    <td port="cls">{resource.cls}</td>
                    <td port="name" bgcolor="white">{name}</td>
                </tr>
            </table>>''',
        }

    def place_node_attr(name: str, place: Place) -> dict[str, str]:
        acquired = ''
        bgcolor = 'lightblue'
        if place.acquired:
            bgcolor = 'cornflowerblue'
            acquired = f'<td port="user" border="0" align="right"><b>{place.acquired}</b></td>'

        tags = '<tr><td border="0" align="left">Tags</td></tr>' if place.tags else ''
        for k, v in place.tags.items():
            tags += f'<tr><td border="0"></td><td border="0" align="left">{k}={v}</td></tr>'

        return {
            'shape': 'plaintext',
            'label': f'''<
            <table bgcolor="{bgcolor}">
                <tr>
                    <td border="0" align="left">Place</td>
                    {acquired}
                </tr>
                <tr>
                    <td port="name" colspan="2" bgcolor="white">{name}</td>
                </tr>
                {tags}
            </table>>''',
        }

    g = graphviz.Digraph('G')
    g.attr(rankdir='LR')

    paths = {}
    for exporter, groups in session.resources.items():
        g_exporter = graphviz.Digraph(f'cluster_{exporter}')
        g_exporter.attr(label=exporter)

        for group, resources in groups.items():
            g_group = graphviz.Digraph(f'cluster_{group}')
            g_group.attr(label=group)

            for r_name, entry in resources.items():
                res_node = f'{exporter}/{group}/{entry.cls}/{r_name}'.replace(':', '_')
                paths[res_node] = [exporter, group, entry.cls, r_name]
                g_group.node(res_node, **res_node_attr(r_name, entry))

            g_exporter.subgraph(g_group)

        g.subgraph(g_exporter)

    for p_node, place in session.places.items():
        g.node(p_node, **place_node_attr(p_node, place))

        for m in place.matches:
            for node, p in paths.items():
                if m.ismatch(p):
                    g.edge(
                        f'{node}:name', p_node,
                        style='solid' if place.acquired else 'dotted',
                        label=m.rename if m.rename else None,
                    )

    return g.pipe(format='svg')


async def get_status(request):
    global session
    raw_svg = await do_graph(session)
    svg = raw_svg.decode()
    return web.Response(text=svg, content_type="image/svg+xml")


async def main_page(request):
    with open("output/status.html") as f:
        page = f.read()
    return web.Response(text=page, content_type="text/html")


async def get_configs(request):
    path = CONFIGS_DIR.glob("*")
    files = [file for file in path if file.is_file()]
    data = []
    for file in files:
        stat = os.stat(file)
        data.append(
            dict(
                name=file.name,
                path=str(file),
                mtime=str(datetime.datetime.fromtimestamp(stat.st_mtime)),
                size=stat.st_size,
            )
        )
    return web.Response(text=json.dumps(data))


async def read_config(request):
    filename = request.match_info.get("file", None)
    path = CONFIGS_DIR / pathlib.Path(filename)
    if not path.exists():
        return web.Response(text=f"File '{filename}' doesn't exist", status=404)
    with open(path) as f:
        content = f.read()
    return web.Response(text=content)


async def configs_page(request):
    with open("output/configs.html") as f:
        page = f.read()
    return web.Response(text=page, content_type="text/html")


async def async_main(host, port):
    app = web.Application()
    app.add_routes(
        [
            web.get('/', main_page),
            web.get('/status', main_page),
            web.get('/configs', configs_page),
            web.get('/api/configs', get_configs),
            web.get('/api/configs/{file}', read_config),
            web.get('/api/status', get_status),
        ]
    )
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info(f"Server started at '{host}:{port}'")

    while True:
        await asyncio.sleep(3600)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080, help="server port")
    parser.add_argument(
        '--coordinator',
        '-x',
        metavar='URL',
        default=os.environ.get('LG_COORDINATOR', '127.0.0.1:20408'),
        help='Coordinator address as HOST[:PORT] (default: %(default)s)',
    )
    args = parser.parse_args()

    global session

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        session = start_session(
            args.coordinator,
            loop=loop,
        )
    except ConnectionRefusedError:
        logger.fatal('Unable to connect to labgrid coordinator')
        return 1

    asyncio.run(async_main(socket.gethostname(), args.port))
    loop.run_until_complete(session.stop())
    loop.run_until_complete(session.close())


if __name__ == "__main__":
    sys.exit(main())
