import subprocess as sp
import os
import time
import threading
import telebot

#from bot_control_v12_add_checknode import cmd_result

TOKEN = ''
with open('../t_test.txt', 'r') as f:
    for i in f:
        TOKEN = i

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot=bot)
stand = ['dev.txt', 'uat.txt', 'pprod.txt']
#user_id_g = '234769242'
bot_tele = telebot.TeleBot(TOKEN)

def result_dns_split(str):
    if len(str) > 4096:
        for x in range(0, len(str), 4096):
            yield str[x:x + 4096]
    else:
        yield str

#cur.execute(f'SELECT userid FROM users')
#user_id_g = cur.fetchall()


def CheckDns():
    global user_id_g
    result_cmd_dns = ''
    if user_id_g:
        print(f' user id g is not null ? {user_id_g}')
        for i in stand:
            print(i)
            os.environ["dns_check_stand"] = f"{i}"
            cmd_dns = sp.Popen(['export DOMAIN=gitlab.akb-it.ru; echo "=> Start DNS resolve test"; kubectl --kubeconfig $dns_check_stand get pods -l name=dnstest --no-headers -o custom-columns=NAME:.metadata.name,HOSTIP:.status.hostIP | while read pod host; do kubectl --kubeconfig $dns_check_stand exec $pod -- /bin/sh -c "nslookup $DOMAIN > /dev/null 2>&1"; RC=$?; if [ $RC -ne 0 ]; then echo $host cannot resolve $DOMAIN; fi; done; echo "=> End DNS resolve test"'], shell=True, encoding="utf8", stdout=sp.PIPE)
            result_cmd_dns += cmd_dns.stdout.read()
            print(str(result_cmd_dns))
        if 'cannot resolve' in result_cmd_dns:
            for i in result_dns_split(result_cmd_dns):
                for (j,) in user_id_g:
                    try:
                        bot_tele.send_message(i, j)
                    except telebot.apihelper.ApiTelegramException:
                        print(j)
            time.sleep(300)





def th_check_dns():
    while True:
        time.sleep(3)
        CheckDns()


th2 = threading.Thread(target=th_check_dns)
th2.start()

# if __name__ == '__main__':
#    executor.start_polling(dp)
