from datetime import datetime


from aiogram import types

from loader import dp


from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import State, StatesGroup

class ReminderStates(StatesGroup):
    name = State()
    time = State()
    date = State()



@dp.callback_query_handler(text='add_reminder')
async def add_reminder(call: types.CallbackQuery):
    
        
    await call.message.answer('Введи назву нагадування')
    
    await call.message.edit_text('Введи назву нагадування')
    await ReminderStates.name.set()
    
@dp.message_handler(state=ReminderStates.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введи час нагадування\n(формат: 23:59)')
    await ReminderStates.time.set()
    
@dp.message_handler(state=ReminderStates.time)
async def get_time(message: types.Message, state: FSMContext):
    time = message.text
    try:
        time = datetime.strptime(time, '%H:%M')
    except ValueError:
        await message.answer('Невірний формат часу\nСпробуй ще раз (формат: 23:59 или 18:30)')
        return

    await state.update_data(time=time)
    await message.answer('Введи дату нагадування\n(формат: 01.01.2021)')
    
    await ReminderStates.date.set()
    
@dp.message_handler(state=ReminderStates.date)
async def get_date(message: types.Message, state: FSMContext):
    date = message.text
    try:
        date = datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        await message.answer('Невірний формат дати\nСпробуй ще раз (формат: 01.01.2021)')
        return
    
    await state.update_data(date=date)
    
    data = await state.get_data()
    
    await message.answer('Нагадування додано')
    await message.answer(f'Назва: {data["name"]}\nЧас: {data["time"]}\nДата: {data["date"]}')
    
    await state.finish()