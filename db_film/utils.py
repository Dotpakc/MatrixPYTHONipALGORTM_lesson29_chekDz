import os
import json

from datetime import datetime

# ЗАДАЧІ
# DONE 1.Отримати список фільмів з папки db_film\films.json
# DONE 2.Отримати список дні показу фільмів з папки db_film\rental.json
# DONE 3.Отримати список дні показу фільмів знаючи id фільму відносно сьогоднішньої дати

def get_films():
    films = json.load(open('db_film/films.json', encoding='utf-8'))
    return films

def get_rental():
    rental = json.load(open('db_film/rental.json', encoding='utf-8'))
    return rental

def get_all_rental_by_film(film_id):
    rentals = get_rental()
    film_rental = []
    for rental in rentals:
        if rental['film'] == film_id:
            date_rental = datetime.strptime(rental['date'], '%Y-%m-%d %H:%M:%S')
            if date_rental > datetime.now():
                film_rental.append(rental)
    return film_rental

def get_days_rental_by_film(film_id):
    rentals = get_all_rental_by_film(film_id)
    days = []
    for rental in rentals:
        date_rental = datetime.strptime(rental['date'], '%Y-%m-%d %H:%M:%S')
        if date_rental.date() not in days:
            days.append(date_rental.date())
    return sorted(days)

def get_times_rantal_by_film_and_date(film_id, date):
    rentals = get_all_rental_by_film(film_id)
    times = []
    for rental in rentals:
        date_rental = datetime.strptime(rental['date'], '%Y-%m-%d %H:%M:%S')
        if date_rental.date() == date:
            if date_rental.time() not in times:
                times.append(date_rental.time())
    return sorted(times)

def get_films_in_rental():
    films = get_films()
    films_in_rental = []
    for film in films:
        if len(get_all_rental_by_film(film['id'])) > 0:
            films_in_rental.append(film)
    return films_in_rental




if __name__ == '__main__':
    print(get_films())
    text = 'ФІЛЬМИ\n\n'
    for film in get_films():
        text += f"{film['title']}\n"
        text += f"{film['description']}\n\n"
        text += f"Рейтинг: {film['rating']}\n"
        text += f"Тривалість: {film['duration']}\n"
        text += f"Жанр: {film['genre']}\n"
        text += f"Ціна білету: {film['price']} грн\n\n"
    print(text)
    
    print(get_rental())
    
    print("film_id = 1")
    print(get_all_rental_by_film(1), len(get_all_rental_by_film(1)))
    
    print("film_id = 2")
    print(get_all_rental_by_film(2), len(get_all_rental_by_film(2)))
    print(get_days_rental_by_film(2), len(get_days_rental_by_film(2)))
    print(get_times_rantal_by_film_and_date(2, datetime.strptime('2021-09-01', '%Y-%m-%d').date()))
    print(get_times_rantal_by_film_and_date(2, datetime.strptime('2023-07-22', '%Y-%m-%d').date()))
    