import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from database import getlessons

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатуры
inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1", callback_data='01'),
         InlineKeyboardButton(text="2", callback_data='02')],
        [InlineKeyboardButton(text="3", callback_data='03'),
         InlineKeyboardButton(text="4", callback_data='04')],
        [InlineKeyboardButton(text="5", callback_data='05'),
         InlineKeyboardButton(text="6", callback_data='06')],
        [InlineKeyboardButton(text="Еще", callback_data='other')]
    ]
)

inline_kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="7", callback_data='07'),
         InlineKeyboardButton(text="8", callback_data='08')],
        [InlineKeyboardButton(text="9", callback_data='09'),
         InlineKeyboardButton(text="10", callback_data='010')],
        [InlineKeyboardButton(text="11", callback_data='011')],
        [InlineKeyboardButton(text="Назад", callback_data='back')]
    ]
)

days = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Понедельник", callback_data='3Понедельник'),
         InlineKeyboardButton(text="Вторник", callback_data='3Вторник')],
        [InlineKeyboardButton(text="Среда", callback_data='3Среда'),
         InlineKeyboardButton(text="Четверг", callback_data='3Четверг')],
        [InlineKeyboardButton(text="Пятница", callback_data='3Пятница'),
         InlineKeyboardButton(text="Суббота", callback_data='3Суббота')],
        [InlineKeyboardButton(text="Назад", callback_data='back')]
    ]
)

classes = {
    "01": ["А", "Б", "В"],
    "02": ["А", "Б", "В"],
    "03": ["А", "Б", "В"],
    "04": ["А", "Б", "В"],
    "05": ["А", "Б", "В"],
    "06": ["А", "Б", "В"],
    "07": ["А", "Б", "В"],
    "08": ["А", "Б"],
    "09": ["А", "Б"],
    "010": ["А"],
    "011": ["А", "Б"]
}

def create_table(num):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=a, callback_data=f"7{a}") for a in classes[num]],
            [InlineKeyboardButton(text="Назад", callback_data='back')]
        ]
    )

# Хранение данных пользователя
user_data = {}

@dp.callback_query(lambda query: query.data.startswith('0'))
async def select_class(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    class_num = callback_query.data
    user_data[user_id] = {"class_num": class_num}  # Сохраняем номер класса
    await callback_query.message.edit_text("Укажи свой класс:", reply_markup=create_table(class_num))
    await callback_query.answer()

@dp.callback_query(lambda query: query.data.startswith('7'))
async def select_letter(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    class_letter = callback_query.data[1:]  # Извлекаем букву класса
    user_data[user_id]["class_letter"] = class_letter  # Сохраняем букву класса
    await callback_query.message.edit_text("Укажи день недели:", reply_markup=days)
    await callback_query.answer()

@dp.callback_query(lambda query: query.data.startswith('3'))
async def get_days(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    day = callback_query.data[1:]  # Извлекаем день недели

    # Получаем сохранённые данные
    class_num = user_data.get(user_id, {}).get("class_num")
    class_letter = user_data.get(user_id, {}).get("class_letter")

    if not class_num or not class_letter:
        await callback_query.message.edit_text("Ошибка: данные не найдены.")
        return

    # Получаем расписание
    lessons = getlessons(class_num, class_letter, day)

    if not lessons:
        await callback_query.message.edit_text("На этот день уроков нет.", reply_markup=inline_kb)
        return

    # Формируем текст расписания
    text = "\n".join([f"{lesson[0]} - {lesson[1]} (каб. {lesson[2]})" for lesson in lessons])
    await callback_query.message.edit_text(text, reply_markup=inline_kb)
    await callback_query.answer()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет, это бот по расписанию в нашей школе!")
    await message.answer("Укажи свой класс:", reply_markup=inline_kb)

@dp.callback_query(lambda c: c.data == 'other')
async def show_more_classes(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Укажи свой класс:", reply_markup=inline_kb2)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == 'back')
async def go_back(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Укажи свой класс:", reply_markup=inline_kb)
    await callback_query.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
