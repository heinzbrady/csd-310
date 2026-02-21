# Brady Heinz 7.2 Assignment 2/21/2026

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent / ".env"
secrets = dotenv_values(env_path)

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
}

def show_films(cursor, title):
    query = """
        SELECT
            film.film_name AS Name,
            film.film_director AS Director,
            genre.genre_name AS Genre,
            studio.studio_name AS Studio
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
        ORDER BY film.film_id;
    """

    cursor.execute(query)
    films = cursor.fetchall()

    print(f"\n-- {title} --")
    for name, director, genre, studio in films:
        print(f"Film Name: {name}")
        print(f"Director: {director}")
        print(f"Genre Name ID: {genre}")
        print(f"Studio Name: {studio}\n")


try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Display original films
    show_films(cursor, "DISPLAYING FILMS")

    # INSERT Deadpool
    cursor.execute("""
        INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
        VALUES ('Deadpool', '2016', 108, 'Tim Miller', 1, 4);
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # UPDATE Alien to Horror
    cursor.execute("""
        UPDATE film
        SET genre_id = 1
        WHERE film_name = 'Alien';
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

    # DELETE Gladiator
    cursor.execute("""
        DELETE FROM film
        WHERE film_name = 'Gladiator';
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Invalid credentials")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist")
    else:
        print(err)

finally:
    try:
        cursor.close()
        db.close()
    except:
        pass