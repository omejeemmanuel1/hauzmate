from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from aiogram.types import Update
from app.core import bot, dp
from app.config import WEBHOOK_PATH, FULL_WEBHOOK
import logging

# Setup logger
logger = logging.getLogger("hauzmate")
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("WEBHOOK_PATH:", WEBHOOK_PATH)
    print("FULL_WEBHOOK:", FULL_WEBHOOK)

    await bot.set_webhook(FULL_WEBHOOK)
    yield 
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def welcome():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HauzMate</title>
        <style>
            body { font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .container { text-align: center; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; }
            h1 { color: #333; margin: 0 0 10px; }
            p { color: #666; margin: 10px 0; }
            .button-group { margin-top: 30px; display: flex; gap: 10px; justify-content: center; }
            a { padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; transition: background 0.3s; }
            a:hover { background: #764ba2; }
            a.secondary { background: #48bb78; }
            a.secondary:hover { background: #38a169; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HauzMate</h1>
            <p>Find your perfect space or list your property</p>
            <div class="button-group">
                <a href="https://t.me/HauzMateBot">Start Bot</a>
                <a class="secondary" href="https://t.me/+6hrnpdbiwgg2M2U0">View Listings</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update_dict = await request.json()
    logger.info("Incoming webhook: %s", update_dict)
    update = Update(**update_dict)
    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}
