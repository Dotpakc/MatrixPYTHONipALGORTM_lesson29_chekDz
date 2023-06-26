from aiogram import types

# 1.курси
# 2.Контакти
# 3.Про нас
# 4.Підтримка


main_keyboard = types.InlineKeyboardMarkup(row_width=1)
main_keyboard.add(
    types.InlineKeyboardButton(text='Математична гра', callback_data='math_game'),

    types.InlineKeyboardButton(text='➕Додати нагадування', callback_data='add_reminder')
)

main_back_keyboard = types.InlineKeyboardMarkup(row_width=2)
main_back_keyboard_but =types.InlineKeyboardButton(text='👈 В головне меню', callback_data='main_back')
main_back_keyboard.add(main_back_keyboard_but)