from aiogram import Router, types
from aiogram.filters import Command
from app.config import BANK_NAME, BANK_ACCOUNT, BANK_HOLDER

router = Router()

@router.message(Command("pay"))
async def manual_payment(message: types.Message):
    await message.answer(
        f"<b>💳 Manual Payment Details</b>\n\n"
        f"<b>Bank:</b> <code>{BANK_NAME}</code>\n"
        f"<b>Account Name:</b> <code>{BANK_HOLDER}</code>\n"
        f"<b>Account Number:</b> <code>{BANK_ACCOUNT}</code>\n\n"
        f"⚠️ After payment, send proof here.\n\n"
        f"<i>Thank you for using HauzMate!</i>"
    )