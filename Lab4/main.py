import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432,
                        dbname='wbauer_adb', user='wbauer_adb', password='adb2020')


# Pomocnicza funkcje aby nie duplikować kodu
def insert_good_where_statement(value):
    if isinstance(value, int):
        return 'category.category_id'
    if isinstance(value, str):
        return 'category.name'

# Tutaj nie zwracamy uwagi na wielkość liter
def dont_care_about_letter_size(value):
    if isinstance(value, int):
        return f'category.category_id = {value}'
    if isinstance(value, str):
        return f"category.name ILIKE '{value}' "


def film_in_category(category: Union[int, str]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str, dokładnie taki jak podana wartość
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|

    Tabela wynikowa ma być posortowana po tylule filmu i języku.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category, int) or isinstance(category, str):
        good_where_clause = insert_good_where_statement(category)
        df = pd.read_sql(f"""
        SELECT film.title AS title, language.name AS languge, category.name AS category FROM category
        INNER JOIN film_category ON category.category_id = film_category.category_id
        INNER JOIN film ON film_category.film_id = film.film_id
        INNER JOIN language ON film.language_id = language.language_id
        WHERE {good_where_clause} = %s
        ORDER BY film.title, language.name
        """, con=connection, params=[category])
        return df

    return None


def film_in_category_case_insensitive(category: Union[int, str]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|

    Tabela wynikowa ma być posortowana po tylule filmu i języku.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if isinstance(category, int) or isinstance(category, str):
        good_where_clause = dont_care_about_letter_size(category)
        df = pd.read_sql(f"""
        SELECT film.title AS title, language.name AS languge, category.name AS category FROM category
        INNER JOIN film_category ON category.category_id = film_category.category_id
        INNER JOIN film ON film_category.film_id = film.film_id
        INNER JOIN language ON film.language_id = language.language_id
        WHERE {good_where_clause}
        ORDER BY film.title, language.name
        """, con=connection)
        return df

    return None


def film_cast(title: str) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o obsadę filmu o dokładnie zadanym tytule.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |
    |0	|Greg       |Chaplin    | 

    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    title (int): wartość id kategorii dla którego wykonujemy zapytanie

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(title, str):
        df = pd.read_sql("""
        SELECT first_name, last_name FROM actor
        INNER JOIN film_actor ON actor.actor_id = film_actor.actor_id
        INNER JOIN film ON film_actor.film_id = film.film_id
        WHERE film.title ILIKE %s
        ORDER BY actor.last_name
        """, con=connection, params=[title])
        return df

    return None


def film_title_case_insensitive(words: list):
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuły filmów zawierających conajmniej jedno z podanych słów z listy words.
    Przykład wynikowej tabeli:
    |   |title              |
    |0	|Crystal Breaking 	| 

    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.

    Parameters:
    words(list): wartość minimalnej długości filmu

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(words, list):
        words = '|'.join(words)
        df = pd.read_sql(f"""
        SELECT title FROM film
        WHERE title ~* '(?:^| )({words})""" + """{1,}(?:$| )'
        ORDER BY title
        """, con=connection)
        return df

    return None
