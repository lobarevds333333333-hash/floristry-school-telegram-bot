import logging
from aiohttp import web

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MockCRM")

async def handle_lead_post(request: web.Request):
    """
    Simulates CRM lead reception POST endpoint.
    """
    try:
        data = await request.json()
        logger.info("==========================================")
        logger.info("[MOCK CRM] INCOMING LEAD POST REQUEST:")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Payload: {data}")
        logger.info("==========================================")

        return web.json_response({
            "status": "success",
            "crm_id": 99823,
            "message": "Lead successfully created in Mock CRM",
            "received_data": data
        }, status=200)
    except Exception as e:
        logger.error(f"[MOCK CRM] Error processing request: {e}")
        return web.json_response({
            "status": "error",
            "message": str(e)
        }, status=400)


def create_app():
    app = web.Application()
    app.router.add_post("/api/lead", handle_lead_post)
    return app

if __name__ == "__main__":
    print("[MOCK CRM] Starting Mock CRM Webhook Server on http://127.0.0.1:8000/api/lead ...")
    web.run_app(create_app(), host="127.0.0.1", port=8000)
