import subprocess as sp
import os
import re
import time
import pandas as pd
import threading
import telebot
from users import *

TOKEN = ''
with open('t_test.txt', 'r') as f:
    for i in f:
        TOKEN = i

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot=bot)
stand = ['dev.txt', 'uat.txt', 'pprod.txt']
# user_id_g = []
bot_tele = telebot.TeleBot(TOKEN)

#cur.execute(f'SELECT userid FROM users')
#user_id_g = cur.fetchall()


def CheckNode():
    global user_id_g
    df = None
    result_cmd_g = ''
    if user_id_g:
        print(f' user id g is not null ? {user_id_g}')
        for i in stand:
            print(i)
            os.environ["node_check_stand"] = f"{i}"
            cmd = sp.Popen(['kubectl --kubeconfig $node_check_stand get nodes'], shell=True, encoding="utf8", stdout=sp.PIPE)
            result_cmd_g = cmd.stdout.read()
            result_cmd_g = re.sub(' +', ';', result_cmd_g)
            df = pd.DataFrame([x.split(';') for x in result_cmd_g.split('\n')])
            df = df[df.isin(['NotReady', 'NotReady,SchedulingDisabled']).any(axis=1)]
            if df.empty:
                print(f'df is empty')
                time.sleep(1)
            else:
                for (i,) in user_id_g:
                    print(i)
                    try:
                        bot_tele.send_message(i, str(df.to_csv(header=None, index=False).replace(',', '  ')))
                    except telebot.apihelper.ApiTelegramException:
                        print(i)
                time.sleep(900)
    else:
        print(f' user id g is 0 ? {user_id_g}')
        time.sleep(1)


def th_node_check():
    while True:
        time.sleep(1)
        CheckNode()


th1 = threading.Thread(target=th_node_check)
th1.start()

# if __name__ == '__main__':
#    executor.start_polling(dp)
