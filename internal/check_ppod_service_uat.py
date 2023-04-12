import time
import threading
import telebot
from users import *
import requests

TOKEN = ''
with open('t_test.txt', 'r') as f:
    for i in f:
        TOKEN = i

ppod_ingress_list = []

with open('ppod_ingress_check.txt', 'r') as ingress_list:
    for j in ingress_list:
        ppod_ingress_list.append(j.strip())

bot_tele = telebot.TeleBot(TOKEN)


def CheckServicePpod():
    global user_id_g
    for j in ppod_ingress_list:
        print(j)
        response = requests.get(f'http://{j}')
        print(f' status code {response.status_code}')
        if int(response.status_code) != 200 and int(response.status_code) != 401:
            print(f'not 401')
            for (i,) in user_id_g:
                try:
                    bot_tele.send_message(i, f'ppod_uat_service not 401 alarm {j} response code {response.status_code}')
                except telebot.apihelper.ApiTelegramException:
                    print(f'ppod_uat_service not 401 alarm')


def th_CheckServicePpod():
    while True:
        time.sleep(600)
        CheckServicePpod()


th3 = threading.Thread(target=th_CheckServicePpod)
th3.start()
