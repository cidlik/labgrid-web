#!/usr/bin/env python3

import argparse
import json
import logging
import os
import pathlib
import datetime
import sys

import asyncio
from aiohttp import web


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

CONFIGS_DIR = pathlib.Path("output")


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


async def async_main(port):
    app = web.Application()
    app.add_routes(
        [
            web.get('/', main_page),
            web.get('/status', main_page),
            web.get('/configs', configs_page),
            web.get('/api/configs', get_configs),
            web.get('/api/configs/{file}', read_config),
        ]
    )
    runner = web.AppRunner(app)
    await runner.setup()
    host = "localhost"
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info(f"Server started at '{host}:{port}'")

    while True:
        await asyncio.sleep(3600)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=80, help="server port")
    args = parser.parse_args()

    asyncio.run(async_main(args.port))


if __name__ == "__main__":
    sys.exit(main())
