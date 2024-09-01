#!/usr/bin/env python3

# $ curl http://localhost:8080/relay/1/2
# $ curl http://localhost:8080/relay/1
# $ curl http://localhost:8080/relay/2

import argparse
import logging
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


async def main_page(request):
    with open("output/status.html") as f:
        page = f.read()
    return web.Response(text=page, content_type="text/html")


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
