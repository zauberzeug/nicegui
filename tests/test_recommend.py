from unittest.mock import patch, MagicMock
import sqlite3

from examples.carousel.recommend import connect_to_database, fetch_user_preferences_from_database, fetch_cocktail_data_from_database


def setup_module():
    global conn, cursor, user_id, N
    user_id = 1
    N = 3
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create mock data in memory SQLite
    cursor.execute("""CREATE TABLE user (id INTEGER, username TEXT)""")
    cursor.execute("""CREATE TABLE liquor (id INTEGER, name TEXT, img_src TEXT)""")
    cursor.execute("""CREATE TABLE user_liquor (id INTEGER, user_id INTEGER, liquor_id INTEGER)""")
    cursor.execute("""CREATE TABLE cocktail (id INTEGER, name TEXT, desc TEXT, img_src TEXT)""")
    cursor.execute("""CREATE TABLE cocktail_liquor (id INTEGER, cocktail_id INTEGER, liquor_id INTEGER)""")
    cursor.execute("""CREATE TABLE user_cocktail (id INTEGER, user_id INTEGER, cocktail_id INTEGER, rating INTEGER)""")

    cursor.execute("""INSERT INTO user VALUES (?, ?)""", (user_id, "JohnDoe"))
    cursor.execute("""INSERT INTO liquor VALUES (?, ?, ?)""", (1, "Whiskey", "images/whiskey.jpeg"))
    cursor.execute("""INSERT INTO liquor VALUES (?, ?, ?)""", (2, "Rum", "images/rum.webp"))
    cursor.execute("""INSERT INTO user_liquor VALUES (?, ?, ?)""", (1, user_id, 1))
    cursor.execute("""INSERT INTO user_liquor VALUES (?, ?, ?)""", (2, user_id, 2))
    cursor.execute("""INSERT INTO cocktail VALUES (?, ?, ?, ?)""",
                   (1, "Old Fashioned", "Classic whiskey cocktail", "images/old_fashion.jpeg"))
    cursor.execute("""INSERT INTO cocktail_liquor VALUES (?, ?, ?)""", (1, 1, 1))
    cursor.execute("""INSERT INTO user_cocktail VALUES (?, ?, ?, ?)""", (1, user_id, 1, 5))

    cursor.execute("""INSERT INTO cocktail VALUES (?, ?, ?, ?)""",
                   (2, "Mojito", "A refreshing rum cocktail", "images/mojito.jpeg"))
    cursor.execute("""INSERT INTO cocktail_liquor VALUES (?, ?, ?)""", (2, 2, 2))
    cursor.execute("""INSERT INTO user_cocktail VALUES (?, ?, ?, ?)""", (2, user_id, 2, 4))

    conn.commit()

    return conn, cursor


@patch('sqlite3.connect')
def test_connect_to_database(mock_connect):
    mock_connect.return_value = conn
    result = connect_to_database()
    assert result == conn


def test_fetch_user_preferences_from_database():
    result = fetch_user_preferences_from_database(cursor, user_id)
    assert result == ["Whiskey", "Rum"]


def test_fetch_cocktail_data_from_database():
    conn, cursor = setup_module()
    result = fetch_cocktail_data_from_database(cursor, [])  # Pass some actual event ids if needed
    assert result == (
        [1, 2],
        ['Classic whiskey cocktail', 'A refreshing rum cocktail'],
        ['Whiskey', 'Rum']
    )
    cursor.close()
    conn.close()

