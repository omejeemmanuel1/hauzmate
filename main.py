from fastapi import FastAPI, Request
from app.core import bot, dp
from app.config import WEBHOOK_PATH, FULL_WEBHOOK

app = FastAPI()

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = await request.json()
    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}

@app.on_event("startup")
async def startup():
    await bot.set_webhook(FULL_WEBHOOK)