import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

DB_FILE = "db.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add("🎁 Подарки")
menu.add("🎒 Инвентарь")

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    data = load_data()
    user_id = str(msg.from_user.id)

    if user_id not in data:
        data[user_id] = {
            "balance": 100,
            "items": []
        }
        save_data(data)

    await msg.answer(
        "🟡 NFT SIM\n\n"
        "💰 Баланс: 100",
        reply_markup=menu
    )

@dp.message_handler(lambda msg: msg.text == "🎁 Подарки")
async def gifts(msg: types.Message):
    await msg.answer(
        "🎁 Магазин:\n\n"
        "1. 🔥 Fire Gift — 50\n"
        "2. 💎 Diamond Box — 100\n\n"
        "Напиши номер"
    )

@dp.message_handler(lambda msg: msg.text == "🎒 Инвентарь")
async def inventory(msg: types.Message):
    data = load_data()
    user_id = str(msg.from_user.id)

    items = data.get(user_id, {}).get("items", [])

    if not items:
        await msg.answer("📭 Пусто")
        return

    text = "🎒 Твои NFT:\n\n"
    for item in items:
        text += f"• {item}\n"

    await msg.answer(text)

@dp.message_handler()
async def buy(msg: types.Message):
    data = load_data()
    user_id = str(msg.from_user.id)

    if user_id not in data:
        return

    if msg.text == "1":
        data[user_id]["items"].append("🔥 Fire Gift")
    elif msg.text == "2":
        data[user_id]["items"].append("💎 Diamond Box")
    else:
        return

    save_data(data)
    await msg.answer("✅ Куплено")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
