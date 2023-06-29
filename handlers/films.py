from datetime import datetime

from aiogram import types
from loader import dp


from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import State, StatesGroup

from db_film.utils import *

class FilmRental(StatesGroup):
    select_film = State()
    day = State()
    time = State()
    count = State()
    checkout = State()


def gen_keybord_pagination(films, current_page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if current_page == 1:
        markup.add(
            types.InlineKeyboardButton(text='➡️', callback_data=f'page_{current_page+1}')
        )
    elif current_page == len(films):
        markup.add(
            types.InlineKeyboardButton(text='⬅️', callback_data=f'page_{current_page-1}')
        )
    else:
        markup.add(
            types.InlineKeyboardButton(text='⬅️', callback_data=f'page_{current_page-1}'),
            types.InlineKeyboardButton(text='➡️', callback_data=f'page_{current_page+1}')
        )
    return markup


@dp.callback_query_handler(text='films')
async def show_films(call: types.CallbackQuery, state: FSMContext):
    films = get_films_in_rental() # Отримуємо список фільмів які є в прокаті
    film  = films[0]
    
    trailer = film['trailer']
    image = film['image']
    
    markup = gen_keybord_pagination(films)
    markup.add(
        types.InlineKeyboardButton(text='🎬 Трейлер на ютуб', url=trailer),
        types.InlineKeyboardButton(text='🎬 Трейлер', callback_data='trailer'),
        types.InlineKeyboardButton(text='🎟️ Купити квиток', callback_data='buy_ticket'),
        types.InlineKeyboardButton(text='👈 В головне меню', callback_data='main_back')
    )
    
    text = f'🎬 <b>Фільм в прокаті:</b>\n\n'
    text += f"<b>Назва:</b> {film['title']}\n"
    text += f"<b>Опис:</b> {film['description']}\n\n"
    text += f"<b>Рейтинг:</b> {film['rating']}\n"
    text += f"<b>Тривалість:</b> {film['duration']}\n"
    text += f"<b>Жанр:</b> {film['genre']}\n"
    text += f"<b>Ціна білету:</b> {film['price']} грн\n"
    
    await call.message.answer_photo(image, caption=text, reply_markup=markup, parse_mode='HTML')
    await call.message.delete()
    
    await FilmRental.select_film.set()
    
    await state.update_data(film = film)
    
@dp.callback_query_handler(text='trailer', state=FilmRental.select_film)
async def show_trailer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    film = data.get('film')
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='👈 Назад', callback_data=f'page_{film["id"]}')
    )
    await call.message.answer(f"<a href='{film['trailer']}'>🎬 {film['title']}</a>\n{film['trailer']}", parse_mode='HTML', reply_markup=markup)
    await call.message.delete()
    
@dp.callback_query_handler(text_contains='page_', state=FilmRental.select_film)
async def show_films_page(call: types.CallbackQuery, state: FSMContext):
    films = get_films_in_rental() # Отримуємо список фільмів які є в прокаті
    film_id = int(call.data.split('_')[-1])
    film  =  films[film_id-1]
    
    trailer = film['trailer']
    image = film['image']
    
    markup = gen_keybord_pagination(films, current_page=film_id)
    markup.add(
        types.InlineKeyboardButton(text='🎬 Трейлер на ютуб', url=trailer),
        types.InlineKeyboardButton(text='🎬 Трейлер', callback_data='trailer'),
        types.InlineKeyboardButton(text='🎟️ Купити квиток', callback_data='buy_ticket'),
        types.InlineKeyboardButton(text='👈 В головне меню', callback_data='main_back')
    )
    
    text = f'🎬 <b>Фільм в прокаті:</b>\n\n'
    text += f"<b>Назва:</b> {film['title']}\n"
    text += f"<b>Опис:</b> {film['description']}\n\n"
    text += f"<b>Рейтинг:</b> {film['rating']}\n"
    text += f"<b>Тривалість:</b> {film['duration']}\n"
    text += f"<b>Жанр:</b> {film['genre']}\n"
    text += f"<b>Ціна білету:</b> {film['price']} грн\n"
    
    await call.message.answer_photo(image, caption=text, reply_markup=markup, parse_mode='HTML')
    await call.message.delete()
    
    await FilmRental.select_film.set()
    
    await state.update_data(film = film)