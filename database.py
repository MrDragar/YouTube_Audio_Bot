import sqlite3
from downloader import wrap

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect("database.db")
    return __connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    userid INTEGER,
    username TEXT);
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS main_information(
    field TEXT,
    value INTEGER);
    """)
    conn.commit()
    cur.execute("""INSERT INTO main_information (field, value)
    SELECT * FROM (SELECT 'count_users', 0) AS tmp
    WHERE NOT EXISTS (
        SELECT field FROM main_information WHERE field = 'count_users'
    ) LIMIT 1;
    """)
    cur.execute("""INSERT INTO main_information (field, value)
    SELECT * FROM (SELECT 'good_result', 0) AS tmp
    WHERE NOT EXISTS (
        SELECT field FROM main_information WHERE field = 'good_result'
    ) LIMIT 1;
    """)
    cur.execute("""INSERT INTO main_information (field, value)
    SELECT * FROM (SELECT 'bad_result', 0) AS tmp
    WHERE NOT EXISTS (
        SELECT field FROM main_information WHERE field = 'bad_result'
    ) LIMIT 1;
    """)
    conn.commit()


def add_user(user_id, username):
    conn = get_connection()
    cur = conn.cursor()
    info = cur.execute("""SELECT * FROM users WHERE userid=?""", (user_id,))

    if info.fetchone() is None:
        print(1, username)
        cur.execute("""INSERT INTO users (userid, username) VALUES (?, ?)""", (user_id, username))
        count_users = cur.execute("""SELECT * FROM main_information WHERE field='count_users'""")
        cur.execute("""UPDATE main_information SET value=? WHERE field='count_users'""",
                    (count_users.fetchone()[1]+1, ))
        conn.commit()


def add_good_result():
    conn = get_connection()
    cur = conn.cursor()
    good_result = cur.execute("""SELECT * FROM main_information WHERE field='good_result'""")
    cur.execute("""UPDATE main_information SET value=? WHERE field='good_result'""",
                (good_result.fetchone()[1] + 1,))
    conn.commit()


def add_bad_result():
    conn = get_connection()
    cur = conn.cursor()
    bad_result = cur.execute("""SELECT * FROM main_information WHERE field='bad_result'""")
    cur.execute("""UPDATE main_information SET value=? WHERE field='bad_result'""",
                (bad_result.fetchone()[1] + 1,))
    conn.commit()
