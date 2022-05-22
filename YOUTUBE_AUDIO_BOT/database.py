import logging
import sqlite3
from YOUTUBE_AUDIO_BOT.messages import languages

def get_connection():
    __connection = sqlite3.connect("database1.db")
    return __connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        userid INTEGER,
        username TEXT,
        language TEXT);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS media(
        id INTEGER PRIMARY KEY,
        linkid TEXT,
        type TEXT,
        fileid TEXT,
        resolution TEXT);
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


def add_user(user_id, username, language):
    conn = get_connection()
    cur = conn.cursor()
    info = cur.execute("""SELECT * FROM users WHERE userid=?""", (user_id,))
    if language not in languages:
        language = "en"
    if info.fetchone() is None:
        logging.info(f"Новый пользователь {username}")
        cur.execute("""INSERT INTO users (userid, username, language) VALUES (?, ?, ?)""",
                    (user_id, username, language))
        count_users = cur.execute("""SELECT * FROM main_information WHERE field='count_users'""")
        cur.execute("""UPDATE main_information SET value=? WHERE field='count_users'""",
                    (count_users.fetchone()[1] + 1,))
        conn.commit()


def add_good_result():
    conn = get_connection()
    cur = conn.cursor()
    good_result = cur.execute("""SELECT * FROM main_information WHERE field='good_result'""")
    cur.execute("""UPDATE main_information SET value=? WHERE field='good_result'""",
                (good_result.fetchone()[1] + 1,))
    conn.commit()


def add_bad_result ():
    conn = get_connection()
    cur = conn.cursor()
    bad_result = cur.execute("""SELECT * FROM main_information WHERE field='bad_result'""")
    cur.execute("""UPDATE main_information SET value=? WHERE field='bad_result'""",
                (bad_result.fetchone()[1] + 1,))
    conn.commit()


def change_language(new_language, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE users SET language=? WHERE userid=?""", (new_language, user_id))
    conn.commit()


def get_language(user_id):
    conn = get_connection()
    cur = conn.cursor()
    language = cur.execute("""SELECT * FROM users WHERE userid=?""", (user_id,))
    return language.fetchone()[3]


def get_file_id(media_tipe, linkid, resolution=None):
    conn = get_connection()
    cur = conn.cursor()
    fileid = cur.execute("""SELECT * FROM media WHERE linkid=? AND type=? AND resolution IS ?""",
                         (linkid, media_tipe, resolution)).fetchone()
    if fileid is not None:
        fileid = fileid[3]
    return fileid


def add_file_id(media_type, linkid, fileid, resolution=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO media (linkid, type, fileid, resolution) VALUES (?, ?, ?, ?)""",
                (linkid, media_type, fileid, resolution))
    conn.commit()


def get_all_id():
    conn = get_connection()
    cur = conn.cursor()
    ids = [user[0] for user in cur.execute("""SELECT userid FROM users""").fetchall()]
    return ids

