import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set. Set BOT_TOKEN in environment variables (do not commit .env).")

_group_id = os.getenv("GROUP_ID")
if _group_id is None:
    raise RuntimeError("GROUP_ID not set. Set GROUP_ID (telegram group id) in environment variables.")
try:
    GROUP_ID = int(_group_id)
except ValueError:
    raise RuntimeError("GROUP_ID must be an integer (e.g. -1001234567890).")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL not set. Set WEBHOOK_URL to your HTTPS base URL.")

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
FULL_WEBHOOK = f"{WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

BANK_NAME = os.getenv("BANK_NAME", "Your Bank")
BANK_ACCOUNT = os.getenv("BANK_ACCOUNT", "")
BANK_HOLDER = os.getenv("BANK_HOLDER", "")