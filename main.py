import json
import sqlite3
import requests

# connect

url = "https://ghibliapi.herokuapp.com/films/"
r = requests.get(url)
films = r.json()

# json

file = open("films.json", "w")
file.write(json.dumps(films, sort_keys=True, indent=4, separators=(',', ': ')))

# sqlite

conn = sqlite3.connect("films.sqlite")
cursor = conn.cursor()

# create table if not exists

cursor.execute('''CREATE TABLE IF NOT EXISTS films
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR (100),
                release_date INTEGER,
                producer VARCHAR (100));''')

# write data

film_list = []

for film in films:
    film_info = (film["title"], film["producer"], film["release_date"])
    film_list.append(film_info)

query = "INSERT INTO films (title, producer, release_date) VALUES (?, ?, ?)"
cursor.executemany(query, film_list)
conn.commit()

conn.close()