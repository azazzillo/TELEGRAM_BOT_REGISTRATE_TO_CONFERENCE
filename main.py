# Python
import logging
import os
from datetime import datetime

# Aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram_datepicker import Datepicker, DatepickerSettings

# Local
from settings.answers import HELP_START
from func_my.all_func import *


logging.basicConfig(level=logging.INFO)

bot = Bot(token='7021362704:AAGIM2MiF7PF54jh87WypFS3CXjV_PsZLxg')
storage = MemoryStorage()
dp = Dispatcher(bot ,storage=storage ,run_tasks_by_default=True)

today = datetime.today()
today = str(today)
today = today.split(" ")[0]
today = today.split("-")
today = today[0]+today[1]
today = str(today)


def _get_datepicker_settings():
    return DatepickerSettings() #some settings


inline_btn_1 = InlineKeyboardButton('Зарегестрироваться', callback_data='reg')
inline_btn_2 = InlineKeyboardButton('Зарегестрированные мной', callback_data='my_rec')
inline_btn_3 = InlineKeyboardButton('Отчет', callback_data='all')

inline_kb1 = InlineKeyboardMarkup(row_width=2)
inline_kb1.add(inline_btn_1)
inline_kb1.add(inline_btn_2)
inline_kb1.add(inline_btn_3)


def inline_kb2():
    time_keyboard = InlineKeyboardMarkup()
    for i in range(9, 23):
        time_keyboard.add(InlineKeyboardButton(f'{i}:00', callback_data=f'time_{i}'))
    return time_keyboard

class user_reg(StatesGroup):
    user_firstname = State()
    date = State()
    time = State()
    description = State()

user_data: dict = {}



@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.reply("⬇️", reply_markup=inline_kb1)


@dp.callback_query_handler(lambda c: c.data == 'all', state='*')
async def get_all(callback_query: CallbackQuery):
    result = get_all_records()
    print(result)
    stroka = ""
    for i in result:
        dat = str(i[4]).split(" ")[0]
        print(dat)
        stroka += f'''
Пользователь: {i[1]}
Дата: {i[3]} Время: {i[4]}
'''

    await callback_query.message.answer(stroka)


@dp.callback_query_handler(lambda c: c.data == 'my_rec', state='*')
async def get_my_conf(callback_query: CallbackQuery):
    print("DATTAAAAAAAAMYREC")
    data = get_my_records(data=str(callback_query.from_user.id))
    stroka = ""
    for i in data:
        stroka += f'''
{i[3]}  {i[4]}
Причина: {i[5]}
'''
    await callback_query.message.answer(stroka)


@dp.callback_query_handler(lambda c: c.data == 'reg', state='*')
async def process_registration(callback_query: CallbackQuery):
    datepicker = Datepicker(_get_datepicker_settings())
    markup = datepicker.start_calendar()
    await bot.send_message(callback_query.from_user.id, 'Выберите дату:', reply_markup=markup)
    await callback_query.answer()


@dp.callback_query_handler(Datepicker.datepicker_callback.filter())
async def _process_datepicker(callback_query: CallbackQuery, callback_data: dict):
    global user_data
    datepicker = Datepicker(_get_datepicker_settings())
    date = await datepicker.process(callback_query, callback_data)
    if date:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await callback_query.message.answer(date.strftime('Вы выбрали дату: %d %b'))
        user_data["user_firstname"] = f"{callback_query.from_user.first_name}"
        user_data["datee"] = date.strftime('%m %d %Y')
        await bot.send_message(callback_query.from_user.id, "Выберите время:", reply_markup=inline_kb2())
        await user_reg.time.set()
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=user_reg.time)
async def _process_timepicker(callback_query: CallbackQuery):
    global user_data

    hour = int(callback_query.data.split("_")[1])
    selected_time = datetime.strptime(f"{hour}:00", "%H:%M").time()
    await callback_query.message.answer(f"Вы выбрали время: {selected_time.strftime('%H:%M')}")
    user_data['timee'] = f"{hour}:00"
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "Напишите причину")
    await user_reg.description.set()
    await callback_query.answer()


@dp.message_handler(state=user_reg.description)
async def description_last(message: Message, state: FSMContext):
    global user_data
    description = message.text
    await state.update_data(description=description)
    user_data["description"] = str(description)
    user_data["chat_id"] = str(message.from_id)
    result = registrate(user_data)
    if result == 1:
        await message.answer("Ой! Похоже, что вы уже записаны на эту конференцию")
    else:
        await message.answer(
        f'''
Вы записались на конференцию!
Дата: {user_data["datee"]}
Время: {user_data["timee"]}
''')
    await state.finish() 
    await message.answer("⬇️", reply_markup=inline_kb1)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)