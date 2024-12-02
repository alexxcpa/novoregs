import sqlite3
import datetime

DB_PATH = '../database/hello_bot.db'


def add_user(partner_id: int,
             chat_id: int,
             user_name: str,
             first_name: str,
             last_name: str):

    created_at = datetime.date.today()
    if user_name is None:
        user_name = 'None'
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.execute(f"""INSERT INTO hello_bot (partner_id, chat_id, created_at, user_name, first_name, last_name)
                                VALUES ('{partner_id}', '{chat_id}', '{created_at}', '{user_name}', 
                                '{first_name}', '{last_name}') """)
    db.commit()
    db.close()
    return True


def get_tg_user_id(chat_id: int):
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    db_res = cur.execute(f"""SELECT chat_id FROM hello_bot WHERE chat_id = {chat_id}""").fetchone()
    db.commit()
    db.close()
    if db_res is not None:
        return True
    return False

def get_partner_from_crm(partner_id: int):
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    db_res = cur.execute(f"""SELECT partner_id FROM crm_main WHERE partner_id = {partner_id}""").fetchone()
    db.commit()
    db.close()
    if db_res is not None:
        return True
    return False

def validation_by_chat_id(chat_id: int):
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    db_res = cur.execute(f"""SELECT partner_id, chat_id FROM hello_bot WHERE chat_id = {chat_id}""").fetchone()
    db.commit()
    db.close()
    print(db_res)
    if db_res is not None:
        partner = {
            "partner_id": db_res[0],
            "chat_id": db_res[1]
        }
        return partner
    return False

def validation_by_partner_id(partner_id: int):
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    db_res = cur.execute(f"""SELECT partner_id FROM hello_bot WHERE partner_id = {partner_id}""").fetchone()
    db.commit()
    db.close()
    if db_res is not None:
        return True
    return False

def get_chat_id_by_partner(partner_id: int):
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    db_res = cur.execute(f"""SELECT chat_id FROM hello_bot WHERE partner_id = {partner_id}""").fetchone()
    db.commit()
    db.close()
    if db_res is not None:
        return db_res[0]
    return False


def create_new_table():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.execute(""" CREATE TABLE hello_bot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id integer DEFAULT 0,
        chat_id integer DEFAULT 0,
        created_at date,
        user_name text DEFAULT None,
        first_name text DEFAULT None,
        last_name text DEFAULT None) 
        """)
    db.commit()
    db.close()
