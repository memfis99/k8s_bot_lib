import requests

GITLAB_TOKEN = ''
GITLAB_URL_OPENED = 'https://gitlab.akb-it.ru/api/v4/projects/10295/issues?state=opened'

with open('internal/t_gitlab.txt', 'r') as t_gitlab:
    for i in t_gitlab:
        GITLAB_TOKEN += i


def get_info_opened():
    issue = ''
    global GITLAB_TOKEN, GITLAB_URL_OPENED
    authorization = f'Bearer {GITLAB_TOKEN.strip()}'
    headers = {"Authorization": authorization}
    r = requests.get(GITLAB_URL_OPENED, headers=headers)
    data = r.json()
    if len(data) != 0:
        for i in data:
            iid = i['iid']
            title = i['title']
            description = i['description']
            author = i['author']['name']
            try:
                assignees = i['assignees'][0]['name']
            except IndexError:
                assignees = 'No assignees'
            created_at = i['created_at']
            yield (
                f'iid: {iid}\nauthor: {author}\nassignees: {assignees}\ncreated_at: {created_at}\ntitle: {title}\ndescription: {description}\n##################\n')
    else:
        yield (f'#############\nNo open issue\n#############\n')

# for j in get_info_opened():
#    print(j)
