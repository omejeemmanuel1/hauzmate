import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # "https://mydomain.com"
WEBHOOK_PATH = "/webhook"
FULL_WEBHOOK = f"{WEBHOOK_URL}{WEBHOOK_PATH}"

BANK_NAME = os.getenv("BANK_NAME", "Your Bank")
BANK_ACCOUNT = os.getenv("BANK_ACCOUNT")
BANK_HOLDER = os.getenv("BANK_HOLDER")