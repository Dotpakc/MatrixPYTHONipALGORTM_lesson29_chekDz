import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from keyboards.main_kb import *



from aiogram.dispatcher.filters.state import State, StatesGroup

class MathGame(StatesGroup):
    game = State()
    
stop_keyboard_btn = types.InlineKeyboardButton(text='Зупинити гру', callback_data='stop_math_game')    
    
    
def gen_example(level=1):
    znak = ['+', '-', '*']
    if level == 1:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        example = f'{a} {random.choice(znak)} {b}'
        answer = eval(example)
    elif level == 2:
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        c = random.randint(1, 20)
        example = f'{a} {random.choice(znak)} {b} {random.choice(znak)} {c}'
        answer = eval(example)
    return example, answer
    
def gen_math_keyboard(count=4,level=1):
    exemples = {}
    while len(exemples) < count:
        example, answer = gen_example(level)
        if answer not in exemples:
            exemples[answer] = example
    
    math_keyboard = types.InlineKeyboardMarkup(row_width=2)
    for answer in exemples:
        math_keyboard.add(types.InlineKeyboardButton(text=exemples[answer], callback_data=str(answer)))
    
    true_example=random.choice(list(exemples.keys()))
    
    return math_keyboard, true_example
    
    
    
    
@dp.callback_query_handler(text='math_game')
async def math_game(call: types.CallbackQuery, state: FSMContext):
    math_keyboard, true_example = gen_math_keyboard()
    text = f'Вибери правильний варіант:\n\n Для Відповіді: {true_example}'
    
    await call.message.edit_text(text=text, reply_markup=math_keyboard)
    
    await MathGame.game.set()
    await state.update_data(true_example=true_example)
    
    

    
@dp.callback_query_handler(text='stop_math_game', state=MathGame.game)
async def stop_math_game(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    score = data.get('score')
    
    text = f'Гра закінчена!\n\nВаш рахунок: {score}'
    
    await call.message.edit_text(text=text, reply_markup=main_back_keyboard)
    await state.finish()



@dp.callback_query_handler(state=MathGame.game)
async def check_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    true_example = data.get('true_example')
    score = data.get('score', 0)
    
    
    if call.data == str(true_example):
        score += 1
        text = 'Вірно!\nБали: {}\n\n'.format(score)
    else:
        text = 'Невірно!\nБали: {}\n\n'.format(score)
        score -= 1

    if score > 5:
        level = 2
    else:
        level = 1
    
    math_keyboard, true_example = gen_math_keyboard(level=level)
    math_keyboard.add(stop_keyboard_btn)
    
    text += f'Вибери правильний варіант:\n\n Для Відповіді: {true_example}'    
    
    await call.message.edit_text(text=text, reply_markup=math_keyboard)
    await state.update_data(true_example=true_example, score=score)    