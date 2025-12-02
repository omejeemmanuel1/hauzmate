# app/core.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from aiogram.types import Update
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.config import BOT_TOKEN, WEBHOOK_PATH, FULL_WEBHOOK
from app.middleware import LoggingMiddleware
from app.payments import router as payments_router
import logging

logger = logging.getLogger("hauzmate")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

def get_yes_no_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Yes"), KeyboardButton(text="No")]],
        resize_keyboard=True
    )

def get_religion_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Christian")], [KeyboardButton(text="Muslim")], [KeyboardButton(text="Any")]],
        resize_keyboard=True
    )

def get_gender_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Male")], [KeyboardButton(text="Female")], [KeyboardButton(text="Any")]],
        resize_keyboard=True
    )

def get_house_type_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Apartment")], [KeyboardButton(text="House")], [KeyboardButton(text="Room")]],
        resize_keyboard=True
    )

def get_move_in_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="ASAP")], [KeyboardButton(text="1 Month")], [KeyboardButton(text="3 Months")]],
        resize_keyboard=True
    )

class OwnerForm(StatesGroup):
    religion = State()
    location = State()
    amenities = State()
    house_type = State()
    looking_for = State()
    total_rent = State()
    subsequent_pay = State()
    gender = State()
    preference = State()
    contact = State()
    review = State()

class SeekerForm(StatesGroup):
    religion = State()
    location = State()
    house_type = State()
    budget = State()
    gender = State()
    move_in = State()
    preference = State()
    contact = State()
    review = State()

class UserType(StatesGroup):
    user_type = State()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Space Owner")], [KeyboardButton(text="Space Seeker")]],
        resize_keyboard=True
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Welcome to HauzMate!\n\nAre you a space owner or seeker?",
        reply_markup=keyboard
    )
    await state.set_state(UserType.user_type)

@router.message(UserType.user_type, F.text.in_(["Space Owner", "Space Seeker"]))
async def user_type_handler(message: types.Message, state: FSMContext):
    user_type = message.text
    await state.update_data(user_type=user_type)
    if user_type == "Space Owner":
        await state.set_state(OwnerForm.religion)
        await bot.send_message(chat_id=message.from_user.id, text="What's your religion preference you want?", reply_markup=get_religion_keyboard())
    else:
        await state.set_state(SeekerForm.religion)
        await bot.send_message(chat_id=message.from_user.id, text="What's your own religion?", reply_markup=get_religion_keyboard())

@router.message(UserType.user_type)
async def invalid_user_type(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Please select 'Space Owner' or 'Space Seeker'")

@router.message(OwnerForm.religion, F.text.in_(["Christian", "Muslim", "Any"]))
async def owner_religion(message: types.Message, state: FSMContext):
    await state.update_data(religion=message.text)
    await state.set_state(OwnerForm.location)
    await bot.send_message(chat_id=message.from_user.id, text="What's the property location? (e.g., Lagos, Abuja)")

@router.message(OwnerForm.location)
async def owner_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(OwnerForm.house_type)
    await bot.send_message(chat_id=message.from_user.id, text="What type of property?", reply_markup=get_house_type_keyboard())

@router.message(OwnerForm.house_type, F.text.in_(["Apartment", "House", "Room"]))
async def owner_house_type(message: types.Message, state: FSMContext):
    await state.update_data(house_type=message.text)
    await state.set_state(OwnerForm.amenities)
    await bot.send_message(chat_id=message.from_user.id, text="List amenities (e.g., WiFi, Pool, Gym, etc.)")

@router.message(OwnerForm.amenities)
async def owner_amenities(message: types.Message, state: FSMContext):
    await state.update_data(amenities=message.text)
    await state.set_state(OwnerForm.total_rent)
    await bot.send_message(chat_id=message.from_user.id, text="What's the total monthly rent? (amount in numbers)")

@router.message(OwnerForm.total_rent)
async def owner_total_rent(message: types.Message, state: FSMContext):
    try:
        rent = int(message.text)
        await state.update_data(total_rent=rent)
        await state.set_state(OwnerForm.subsequent_pay)
        await bot.send_message(chat_id=message.from_user.id, text="When is rent due? (e.g., 1st of month, end of month)")
    except ValueError:
        await bot.send_message(chat_id=message.from_user.id, text="Please enter a valid amount")

@router.message(OwnerForm.subsequent_pay)
async def owner_subsequent_pay(message: types.Message, state: FSMContext):
    await state.update_data(subsequent_pay=message.text)
    await state.set_state(OwnerForm.gender)
    await bot.send_message(chat_id=message.from_user.id, text="Preferred tenant gender?", reply_markup=get_gender_keyboard())

@router.message(OwnerForm.gender, F.text.in_(["Male", "Female", "Any"]))
async def owner_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(OwnerForm.preference)
    await bot.send_message(chat_id=message.from_user.id, text="Any other preferences? (e.g., no smoking, no pets)")

@router.message(OwnerForm.preference)
async def owner_preference(message: types.Message, state: FSMContext):
    await state.update_data(preference=message.text)
    await state.set_state(OwnerForm.contact)
    await bot.send_message(chat_id=message.from_user.id, text="What's your contact? (Phone or email)")

@router.message(OwnerForm.contact)
async def owner_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    listing = (
        f"<b>SPACE OWNER LISTING</b>\n\n"
        f"<b>Religion:</b> {data['religion']}\n"
        f"<b>Location:</b> {data['location']}\n"
        f"<b>Property Type:</b> {data['house_type']}\n"
        f"<b>Amenities:</b> {data['amenities']}\n"
        f"<b>Monthly Rent:</b> ₦{data['total_rent']:,}\n"
        f"<b>Rent Due:</b> {data['subsequent_pay']}\n"
        f"<b>Preferred Tenant:</b> {data['gender']}\n"
        f"<b>Preferences:</b> {data['preference']}\n"
        f"<b>Contact:</b> {data['contact']}\n\n"
        f"Posted by: @{message.from_user.username or 'Unknown'}"
    )
    await bot.send_message(message.from_user.id, listing, parse_mode="HTML")
    await bot.send_message(message.from_user.id, "Your listing has been sent privately! ✅")
    await state.clear()

@router.message(SeekerForm.religion, F.text.in_(["Christian", "Muslim", "Any"]))
async def seeker_religion(message: types.Message, state: FSMContext):
    await state.update_data(religion=message.text)
    await state.set_state(SeekerForm.location)
    await bot.send_message(chat_id=message.from_user.id, text="Which location are you looking for?")

@router.message(SeekerForm.location)
async def seeker_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(SeekerForm.house_type)
    await bot.send_message(chat_id=message.from_user.id, text="What type of property do you need?", reply_markup=get_house_type_keyboard())

@router.message(SeekerForm.house_type, F.text.in_(["Apartment", "House", "Room"]))
async def seeker_house_type(message: types.Message, state: FSMContext):
    await state.update_data(house_type=message.text)
    await state.set_state(SeekerForm.budget)
    await bot.send_message(chat_id=message.from_user.id, text="What's your budget? (monthly amount)")

@router.message(SeekerForm.budget)
async def seeker_budget(message: types.Message, state: FSMContext):
    try:
        budget = int(message.text)
        await state.update_data(budget=budget)
        await state.set_state(SeekerForm.gender)
        await bot.send_message(chat_id=message.from_user.id, text="Preferred landlord/housemate gender?", reply_markup=get_gender_keyboard())
    except ValueError:
        await bot.send_message(chat_id=message.from_user.id, text="Please enter a valid amount")

@router.message(SeekerForm.gender, F.text.in_(["Male", "Female", "Any"]))
async def seeker_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(SeekerForm.move_in)
    await bot.send_message(chat_id=message.from_user.id, text="When do you want to move in?", reply_markup=get_move_in_keyboard())

@router.message(SeekerForm.move_in, F.text.in_(["ASAP", "1 Month", "3 Months"]))
async def seeker_move_in(message: types.Message, state: FSMContext):
    await state.update_data(move_in=message.text)
    await state.set_state(SeekerForm.preference)
    await bot.send_message(chat_id=message.from_user.id, text="Any special requirements? (e.g., near school, quiet area)")

@router.message(SeekerForm.preference)
async def seeker_preference(message: types.Message, state: FSMContext):
    await state.update_data(preference=message.text)
    await state.set_state(SeekerForm.contact)
    await bot.send_message(chat_id=message.from_user.id, text="What's your contact? (Phone or email)")

@router.message(SeekerForm.contact)
async def seeker_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    listing = (
        f"<b>SPACE SEEKER REQUEST</b>\n\n"
        f"<b>Religion:</b> {data['religion']}\n"
        f"<b>Location:</b> {data['location']}\n"
        f"<b>Property Type:</b> {data['house_type']}\n"
        f"<b>Budget:</b> ₦{data['budget']:,}/month\n"
        f"<b>Preferred Gender:</b> {data['gender']}\n"
        f"<b>Move-in Date:</b> {data['move_in']}\n"
        f"<b>Requirements:</b> {data['preference']}\n"
        f"<b>Contact:</b> {data['contact']}\n\n"
        f"Posted by: @{message.from_user.username or 'Unknown'}"
    )
    await bot.send_message(message.from_user.id, listing, parse_mode="HTML")
    await bot.send_message(message.from_user.id, "Your request has been sent privately! ✅")
    await state.clear()

@router.message()
async def welcome_new_user(message: types.Message):
    if message.new_chat_members:
        for user in message.new_chat_members:
            await message.answer(f"Welcome {user.full_name} to the group! 🎉")

dp.include_router(router)
dp.include_router(payments_router)
dp.update.middleware(LoggingMiddleware())

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(FULL_WEBHOOK)
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def welcome():
    return "<h1>HauzMate is running!</h1>"

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update_dict = await request.json()
    logger.info("Incoming webhook: %s", update_dict)
    update = Update(**update_dict)
    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}
