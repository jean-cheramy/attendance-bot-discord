import asyncio
from aiohttp import web
import logging

log = logging.getLogger(__name__)

async def handle_health(request):
    return web.Response(text="OK", status=200)

async def start_health_server():
    app = web.Application()
    app.add_routes([web.get('/healthz/startup', handle_health)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    log.info("Health check server started on port 8080")

async def heartbeat():
    while True:
        log.info("Heartbeat: bot is alive.")
        await asyncio.sleep(60)
