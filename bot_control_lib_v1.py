import time
import logging
from aiogram import Bot, Dispatcher, executor
from lib_kubernetes.internal.buttons import *
from lib_kubernetes.internal.users import *
import telebot
from kubernetes import client, config

# from node_check_ready import *
# from dns_check_resolv import *
# from check_ppod_service_uat import *
from lib_kubernetes.internal.gitlab_issue import *

ns_list = []
# stand = ['dev.txt', 'uat.txt', 'pprod.txt']

with open('namespace.txt', 'r') as stand_ns:
    for i in stand_ns:
        ns_list.append(i.strip())

TOKEN = ''

with open('t_test.txt', 'r') as f:
    for i in f:
        TOKEN = i

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
bot_tele = telebot.TeleBot(TOKEN)

kube_config = ''
ns_selected = ''


def cmd_result(str):
    if len(str) > 4096:
        for x in range(0, len(str), 4096):
            yield str[x:x + 4096]
    else:
        yield str


@dp.message_handler(commands=['hello', 'start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    user_text = message.text
    cur.execute(f'SELECT userid FROM users WHERE userid = {user_id}')
    all_result = cur.fetchall()
    if not all_result:
        await message.reply(f'you not ADMIN you TG id {user_id} bay bay.')
    else:
        await message.reply(f" please select stand, you TG id {user_id} you ADMIN", reply_markup=key_sel_stand())


@dp.callback_query_handler()
async def start_call_back(call: types.CallbackQuery):
    global kube_config, ns_selected
    stand_data = call.data
    command_data = call.data
    ns_data = call.data
    back_data = call.data
    gitlab_data = call.data
    if stand_data in ['dev', 'uat', 'pprod']:
        kube_config = config.load_kube_config(config_file=f'internal/{stand_data}.txt')
        await call.message.answer(f'selected stand, {stand_data}', reply_markup=key_sel_ns())
    elif ns_data in ns_list:
        ns_selected = ns_data
        await call.message.answer(f'selected ns , {ns_data}', reply_markup=key_sel_cmd())
    elif command_data in ['get_nodes', 'get_pv', 'get_ns', 'get_ingress', 'get_pods', 'get_deploy', 'get_event']:
        answer = globals()[command_data](kube_config, ns_selected)
        for ans in cmd_result(answer):
            try:
                await call.message.answer(ans, reply_markup=key_sel_cmd())
            except:
                await call.message.answer(f'no data in namespace', reply_markup=key_sel_cmd())
    elif back_data in 'Back':
        await call.message.answer(f'select back', reply_markup=key_sel_stand())
    elif gitlab_data in 'gitlab_open_issue':
        for issue in get_info_opened():
            await call.message.answer(issue)


def get_nodes(kube_config, ns_selected):
    result = client.CoreV1Api(kube_config).list_node()
    node_result = ''
    for node in result.items:
        node_result += ("%s\t%s\t%s\n" % (
            node.metadata.name, node.status.addresses[0].address, node.status.conditions[4].reason))
    return node_result.replace('Kubelet', '')


def get_pv(kube_config, ns_selected):
    result = client.CoreV1Api(kube_config).list_namespaced_persistent_volume_claim(namespace=f'{ns_selected}')
    pv_result = ''
    for pv in result.items:
        pv_result += ("%s\t%s\t%s\t%s\t%s\n" % (
            pv.metadata.name, pv.metadata.namespace, pv.spec.storage_class_name, pv.status.phase, pv.status.capacity))
    return pv_result


def get_ns(kube_config, ns_selected):
    result = client.CoreV1Api(kube_config).list_namespace()
    ns_result = ''
    for ns in result.items:
        ns_result += ("%s\t%s\n" % (ns.metadata.name, ns.status.phase))
    return ns_result


def get_ingress(kube_config, ns_selected):
    result = client.NetworkingV1Api(kube_config).list_namespaced_ingress(namespace=f'{ns_selected}')
    ingress_result = ''
    for ingress in result.items:
        ingress_result += (
                    "%s%s--->%s:%s\tip_bal:%s\n----------------------------------------------------------------\n" % (
                ingress.spec.rules[0].host, ingress.spec.rules[0].http.paths[0].path,
                ingress.spec.rules[0].http.paths[0].backend.service.name,
                ingress.spec.rules[0].http.paths[0].backend.service.port.number,
                ingress.status.load_balancer.ingress[0].ip))
    return ingress_result


def get_pods(kube_config, ns_selected):
    result = client.CoreV1Api(kube_config).list_namespaced_pod(namespace=f'{ns_selected}')
    pods_result = ''
    for pods in result.items:
        pods_result += ("%s\t'%s\n" % (pods.status.phase, pods.metadata.name)).replace("'", ' ')
    return pods_result


def get_deploy(kube_config, ns_selected):
    result = client.AppsV1Api(kube_config).list_namespaced_deployment(namespace=f'{ns_selected}')
    deploy_result = ''
    for deploy in result.items:
        deploy_result += (
                "%s\tREADY:%s\%s\n" % (deploy.metadata.name, deploy.status.ready_replicas, deploy.status.replicas))
    return deploy_result


def get_event(kube_config, ns_selected):
    result = client.CoreV1Api(kube_config).list_namespaced_event(namespace=f'{ns_selected}')
    event_result = ''
    for event in result.items:
        event_result += (
                "%s\t%s\t%s\t%s\n----------------------------------------------------------------\n" % (
        event.involved_object.name, event.type, event.message, event.metadata.namespace))
    return event_result


if __name__ == '__main__':
    executor.start_polling(dp)
