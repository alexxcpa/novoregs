import sqlite3
import datetime as dt

def get_partners_2024():
    date = dt.date(2024, 1, 1)
    date_and = dt.datetime(2024, 1, 31)
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    db_res = cur.execute(
        f"""SELECT partner_id, created_at FROM crm_main""").fetchall()
    partners_info_list = []

    for i in db_res:
        created_at = dt.datetime.strptime(i[1], '%Y-%m-%d')
        if created_at.date() >= date:
            partners_info_list.append(str(i[0]))
    db.commit()
    db.close()
    return partners_info_list

def add_leads(partner_id: int, column: str, value):
    db = sqlite3.connect('../challenge_50_days/challenge_50_days.db')
    cur = db.cursor()
    cur.execute(f"""INSERT INTO partners (partner_id, {column})
                                    VALUES ({partner_id}, '{value}') """)
    db.commit()
    db.close()
    return True
def update_partner(partner_id: int, column: str, value):
    db = sqlite3.connect('../challenge_50_days/challenge_50_days.db')
    cur = db.cursor()
    cur.execute(f"UPDATE partners SET {column} = '{value}' WHERE partner_id = '{partner_id}'")
    db.commit()
    db.close()
    return True


def get_partners_list():
    db = sqlite3.connect('../challenge_50_days/challenge_50_days.db')
    cur = db.cursor()
    db_res = cur.execute(f"SELECT partner_id FROM partners").fetchall()
    print(db_res)
    db.commit()
    db.close()
    return True

def create_new_table():
    db = sqlite3.connect('../challenge_50_days/challenge_50_days.db')
    cur = db.cursor()
    cur.execute(""" CREATE TABLE partners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id integer DEFAULT 0,
        manager text,
        week_1 integer DEFAULT 0,
        week_2 integer DEFAULT 0,
        week_3 integer DEFAULT 0,
        week_4 integer DEFAULT 0,
        week_5 integer DEFAULT 0,
        week_6 integer DEFAULT 0,
        week_7 integer DEFAULT 0,
        week_8 integer DEFAULT 0)
        """)
    db.commit()
    db.close()
