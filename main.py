import json
import requests
import datetime
import time

with open('config.json', mode='r') as config:
    conf = json.load(config)
headers = {'Connection': 'close', 'User-Agent': 'Mozilla/5.0',
           'Cookie': f'uid={conf["uid"]};_uuid={conf["_uuid"]};SESSDATA={conf["SESSDATA"]}'}


def get():
    url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid={conf["uid"]}&host_uid={conf["uid"]}&need_top=1&offset_dynamic_id='
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            return resp
        return False
    except Exception as e:
        print(e)


def post(id):
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic'
    try:
        resp = requests.post(url, data={'dynamic_id': id}, headers=headers, timeout=5)
        if resp.status_code == 200:
            return True
        return False
    except Exception as e:
        print(e)


result = []
offset = 0
page = 1
while True:
    print(f'第{page}页，当前offset是\t{offset}')
    resp = get()
    if resp:
        try:
            cards = resp.json()['data']['cards']
            if cards:
                print('当前页面存在内容……')
                for card in cards:
                    dynamic_id = card['desc']['dynamic_id']
                    timestamp = card['desc']['timestamp']
                    if datetime.datetime.fromtimestamp(timestamp).year <= conf['year']:
                        result.append(dynamic_id)
                        while True:
                            if post(dynamic_id):
                                print(f"删除{dynamic_id}成功")
                                break
                            else:
                                time.sleep(1)
                                continue
                offset = resp.json()['data']['next_offset']
                if offset != 0:
                    print('offset获取成功\t', str(offset))
                page += 1
                time.sleep(0.5)
                print(f'第{page}页结束，累计获取到{len(result)}条结果')
            else:
                break
        except Exception:
            print("获取动态完成！")
            break
    else:
        print('请求resp错误')
        time.sleep(1)
        continue
