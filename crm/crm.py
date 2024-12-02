import requests
from database import db
import os
from logs import logger as log

crm_crm_id = "fields[CATEGORY_ID]"
crm_partner_id = "ID"
crm_stage = "fields[STAGE_ID]"
affise_partner_id = "fields[TITLE]"
crm_created_at = "fields[UF_CRM_1709261790943]"
crm_partner_name = "fields[UF_CRM_1714037465666]"
crm_tg = "fields[UF_CRM_AMO_708027]"
crm_email = "fields[UF_CRM_1708078793207]"
crm_phone = "fields[UF_CRM_1708078808665]"
crm_ref_partner = "fields[UF_CRM_1714822165111]"
crm_vk = "fields[UF_CRM_1708078913792]"
crm_skype = "fields[UF_CRM_1708078934463]"
crm_verticals = "fields[UF_CRM_1714668542842]"
crm_sources_exp = "fields[UF_CRM_1714810639093]"
crm_sources_lm = "fields[UF_CRM_1714812130411]"
crm_about_us = "fields[UF_CRM_1714811593180]"
crm_thematics = "fields[UF_CRM_1714811816433]"
crm_exp_years = "fields[UF_CRM_1714812214869]"
crm_sources_type = "fields[UF_CRM_1714812280252]"
crm_solo_or_team = "fields[UF_CRM_1714814343603]"
crm_experience = "fields[UF_CRM_1714814397556]"
crm_segment_onboarding = "fields[UF_CRM_1714817239412]"
crm_segment_payment = "fields[UF_CRM_1716320558509]"
crm_balance = "fields[OPPORTUNITY]"

crm_first_payment_amount = "fields[UF_CRM_1703235325914]"
crm_second_payment_amount = "fields[UF_CRM_1706593335884]"
crm_third_payment_amount = "fields[UF_CRM_1706593377450]"
crm_fourth_payment_amount = "fields[UF_CRM_1708079919557]"
crm_fifth_payment_amount = "fields[UF_CRM_1718909117682]"
crm_last_payment_amount = "fields[UF_CRM_1706593415817]"

crm_first_payment_roi = "fields[UF_CRM_1708079900033]"
crm_common_roi = "fields[UF_CRM_1708079947827]"


stage_new = "C14:NEW"
stage_hello_answer = "C14:PREPAYMENT_INVOIC"
stage_connect_offers = "C14:FINAL_INVOICE"
stage_first_traffic = "C14:EXECUTING"

stage_ballance_1000 = "C14:UC_M3VGWL"
stage_ballance_2000 = "C14:UC_W9246Z"
stage_ballance_3000 = "C14:UC_BO5BXL"
stage_ballance_4000 = "C14:UC_LG3TU0"

stage_first_payment = "C14:UC_NN4CXI"
stage_second_payment = "C14:LOSE"
stage_third_payment = "C14:UC_S3YDZH"
stage_fourth_payment = "C14:UC_ZSSHQS"
stage_fifth_payment = "C14:UC_NSJWL1"
stage_active_partner = "C14:UC_VJ67DZ"
stage_sleep_partner = "C14:UC_R2BU0L"
stage_froder = "C14:WON"



params = {crm_crm_id: 14,
          crm_partner_id: "",
          crm_stage: "",
          affise_partner_id: "",
          crm_created_at: "",
          crm_partner_name: "",
          crm_tg: "",
          crm_email: "",
          crm_phone: "",
          crm_ref_partner: "",
          crm_vk: "",
          crm_skype: "",
          crm_verticals: "",
          crm_sources_exp: "",
          crm_sources_lm: "",
          crm_about_us: "",
          crm_thematics: "",
          crm_exp_years: "",
          crm_sources_type: "",
          crm_solo_or_team: "",
          crm_experience: "",
          crm_segment_onboarding: "",
          crm_segment_payment: "",
          crm_balance: "",
          crm_first_payment_amount: "",
          crm_second_payment_amount: "",
          crm_third_payment_amount: "",
          crm_fourth_payment_amount: "",
          crm_fifth_payment_amount: "",
          crm_last_payment_amount: "",
          crm_first_payment_roi: "",
          crm_common_roi: "",
          }


def crm_deal_update(partner, stage):
    update_deal_url = f"https://lead-magnet.bitrix24.ru/rest/456/x29qpt47k23euvyj/crm.deal.update.json"
    params[affise_partner_id] = partner["partner_id"]
    params[crm_created_at] = partner["created_at"]
    params[crm_partner_name] = partner['name']
    params[crm_ref_partner] = partner['ref_partner']
    params[crm_email] = partner['email']
    params[crm_phone] = partner['phone']
    params[crm_tg] = partner['telegram']
    params[crm_vk] = partner['vk']
    params[crm_skype] = partner['skype']
    params[crm_segment_onboarding] = partner['segment_onboarding']
    params[crm_segment_payment] = partner['segment_payment']
    params[crm_balance] = partner['balance']
    params[crm_exp_years] = partner['exp_years']
    params[crm_solo_or_team] = partner['solo_or_team']
    params[crm_verticals] = partner['verticals']
    params[crm_thematics] = partner['thematics']
    params[crm_sources_exp] = partner['sources_exp']
    params[crm_sources_lm] = partner['sources_lm']
    params[crm_sources_type] = partner['sources_type']
    params[crm_about_us] = partner['about_us']
    params[crm_stage] = stage
    params[crm_first_payment_amount] = partner['first_payment']
    params[crm_second_payment_amount] = partner['second_payment']
    params[crm_third_payment_amount] = partner['third_payment']
    params[crm_fourth_payment_amount] = partner['fourth_payment']
    params[crm_fifth_payment_amount] = partner['fifth_payment']
    params[crm_last_payment_amount] = partner['last_payment']
    params[crm_first_payment_roi] = partner['first_payment_roi']

    params[crm_common_roi] = partner['common_roi']
    params[crm_partner_id] = partner['crm_partner_id']

    log.msg.info(f"Пробуем обновить партнера {params[crm_partner_id]} в crm битрикс")
    r = requests.get(update_deal_url, params=params)
    res = r.json()
    if res['result'] is True:
        log.msg.info(f"Успешно обновили партнера {params[crm_partner_id]}")

def crm_deal_add(partner: dict, stage: str):
    add_deal_url = f"https://lead-magnet.bitrix24.ru/rest/456/x29qpt47k23euvyj/crm.deal.add.json"
    params[affise_partner_id] = partner["partner_id"]
    params[crm_created_at] = partner["created_at"]
    params[crm_partner_name] = partner['name']
    params[crm_ref_partner] = partner['ref_partner']
    params[crm_email] = partner['email']
    params[crm_phone] = partner['phone']
    params[crm_tg] = partner['telegram']
    params[crm_vk] = partner['vk']
    params[crm_skype] = partner['skype']
    params[crm_segment_onboarding] = partner['segment_onboarding']
    params[crm_segment_payment] = partner['segment_payment']
    params[crm_balance] = partner['balance']
    params[crm_exp_years] = partner['exp_years']
    params[crm_solo_or_team] = partner['solo_or_team']
    params[crm_verticals] = partner['verticals']
    params[crm_thematics] = partner['thematics']
    params[crm_sources_exp] = partner['sources_exp']
    params[crm_sources_lm] = partner['sources_lm']
    params[crm_sources_type] = partner['sources_type']
    params[crm_about_us] = partner['about_us']
    params[crm_stage] = stage
    params[crm_first_payment_amount] = partner['first_payment']
    params[crm_second_payment_amount] = partner['second_payment']
    params[crm_third_payment_amount] = partner['third_payment']
    params[crm_fourth_payment_amount] = partner['fourth_payment']
    params[crm_fifth_payment_amount] = partner['fifth_payment']
    params[crm_last_payment_amount] = partner['last_payment']

    params[crm_first_payment_roi] = partner['first_payment_roi']
    params[crm_common_roi] = partner['common_roi']


    log.msg.info(f"Пробуем добавить партнера {partner['partner_id']} в crm битрикс")
    r = requests.get(add_deal_url, params=params)
    res = r.json()
    crm_partner_id = res['result']
    if isinstance(crm_partner_id, int):
        log.msg.info(f"Успешно добавили партнера {partner['partner_id']} в crm битрикс")
        partner_id = partner['partner_id']
        db.add_crm_partner_id(crm_partner_id, partner_id)
    else:
        log.msg.error(f"Не смогли добавить партнера {partner['partner_id']} в crm. {res['result']}")

def crm_deal_delete(crm_id):
    delete_deal = f"https://lead-magnet.bitrix24.ru/rest/456/x29qpt47k23euvyj/crm.deal.delete.json?ID={crm_id}"
    print(f"Пробуем удалить партнера {crm_id} из crm битрикс")
    r = requests.get(delete_deal)
    res = r.json()
    if res['result'] is True:
        print(f"Успешно удалили партнера {crm_id}")



def crm_partners_add(partners_info_list):
    partners_for_crm = db.get_partners_by_id(tuple(int(partner['partner_id']) for partner in partners_info_list))
    for partner in partners_for_crm:
        if partner['crm_partner_id'] == 0:
            crm_deal_add(partner, stage_new)