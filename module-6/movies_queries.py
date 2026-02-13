# Brady Heinz 6.2 Assignment 2/13/26

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

secrets = dotenv_values(".env")  

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT studio_id, studio_name FROM studio;")
    for studio_id, studio_name in cursor.fetchall():
        print(f"Studio ID: {studio_id}")
        print(f"Studio Name: {studio_name}\n")

    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT genre_id, genre_name FROM genre;")
    for genre_id, genre_name in cursor.fetchall():
        print(f"Genre ID: {genre_id}")
        print(f"Genre Name: {genre_name}\n")

    print("\n-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;")
    for film_name, film_runtime in cursor.fetchall():
        print(f"Film Name: {film_name}")
        print(f"Runtime: {film_runtime}\n")

    print("\n-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("""
        SELECT film_name, film_director
        FROM film
        ORDER BY film_director;
    """)
    for film_name, film_director in cursor.fetchall():
        print(f"Film Name: {film_name}")
        print(f"Director: {film_director}\n")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("ERROR: Invalid username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("ERROR: Database does not exist.")
    else:
        print(err)

finally:
    try:
        cursor.close()
    except:
        pass
    try:
        db.close()
    except:
        pass
