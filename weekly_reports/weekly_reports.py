from database import wekly_reports_db as db
import os
import time

from sheets import sheets

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"
SAMPLE_SPREADSHEET_ID = "1X5Op6GMDDrSUbpw-LhTwQsdt3xLDyKV4CUyCPkXWpP4"
AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'

def sheets_update_weekly_reports(reports_list: list):
    service = sheets.update_google_creds()
    print(f"Пробуем добавить статистику за неделю в гугл таблицу")
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "еженедельные отчеты!A2:H",
                 "majorDimension": "COLUMNS",
                 "values": [
                     [report['period'] for report in reports_list],
                     [report['partners'] for report in reports_list],
                     [report['target'] for report in reports_list],
                     [report['send_hello'] for report in reports_list],
                     [report['connect_offers'] for report in reports_list],
                     [report['first_traffic'] for report in reports_list],
                     [report['first_payment'] for report in reports_list]]
                 },
                {"range": "еженедельные отчеты!N2:Q",
                 "majorDimension": "COLUMNS",
                 "values": [
                     [report['balance_1000'] for report in reports_list],
                     [report['balance_2000'] for report in reports_list],
                     [report['balance_3000'] for report in reports_list],
                     [report['balance_4000'] for report in reports_list]]

                 }
            ]

        }
    ).execute()

    print(f"Успешно вставили статистику за неделю в  гугл таблицу")



def sheets_update_metrick_table(reports_list: list):
    service = sheets.update_google_creds()
    print(f"Пробуем добавить статистику за неделю в отчетную таблицу")
    for report in reports_list:
        if '2024-12-01' in str(report['period']):
            column = 'L'
        elif '2024-12-08' in str(report['period']):
            column = 'K'
        elif '2024-12-15' in str(report['period']):
            column = 'J'
        elif '2024-12-22' in str(report['period']):
            column = 'I'
        elif '2024-12-29' in str(report['period']):
            column = 'H'
        else:
            continue

        values = service.spreadsheets().values().batchUpdate(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"отчетная таблица!{column}2",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['partners']]]
                     },
                    {"range": f"отчетная таблица!{column}3",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['target']]]
                     },
                    {"range": f"отчетная таблица!{column}5",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['send_hello']]]
                     },
                    {"range": f"отчетная таблица!{column}7",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['connect_offers']]]
                     },
                    {"range": f"отчетная таблица!{column}10",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['first_traffic']]]
                     },
                    {"range": f"отчетная таблица!{column}11",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['balance_1000']]]
                     },
                    {"range": f"отчетная таблица!{column}12",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['balance_2000']]]
                     },
                    {"range": f"отчетная таблица!{column}13",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['balance_3000']]]
                     },
                    {"range": f"отчетная таблица!{column}14",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['balance_4000']]]
                     },


                    {"range": f"отчетная таблица!{column}21",
                     "majorDimension": "COLUMNS",
                     "values": [
                         [report['first_payment']]]
                     },
                ]

            }
        ).execute()

        print(f"Успешно вставили статистику за неделю в  гугл таблицу")
        time.sleep(0.5)


def weekly_reports():
    res = db.get_weekly_reports()
    sheets_update_weekly_reports(res)
    sheets_update_metrick_table(res)

weekly_reports()
