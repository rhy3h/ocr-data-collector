import argparse
import json
import base64
import os
import time

import requests

CACA_QUEST_URL = 'https://gen.caca01.com/ttcode/quest'
CACA_TEST_URL = 'https://gen.caca01.com/rd/test'

ROOT_PATH = 'dataset/tixcraft'

def saveData(text: str):
    data_list = json.loads(text)

    code_list = data_list['codelist']
    for code in code_list:
        id = code['id']
        image = code['code']
        ans = code['ans']

        img_data = base64.b64decode(image)

        with open(f'{ROOT_PATH}/{id}_{ans}.png', 'wb') as f:
            f.write(img_data)

def getQuestData():
    resp = requests.get(CACA_QUEST_URL)
    saveData(resp.text)

def getTestData():
    resp = requests.get(CACA_TEST_URL)
    saveData(resp.text)

def main(loop: int):
    os.makedirs(ROOT_PATH, exist_ok=True)

    for i in range(loop):
        print(f'{i + 1} / {loop}')
        getQuestData()
        getTestData()

        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make multiple requests')
    parser.add_argument('--loop', type=int, default=1, help='Number of iterations (default: 1)')

    args = parser.parse_args()

    main(args.loop)
