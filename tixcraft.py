import argparse
import json
import base64
import os

from typing import Dict

import requests
from pathlib import Path

from ocr import Ocr, PredictInfo

CACA_QUEST_URL = 'https://gen.caca01.com/ttcode/quest'
CACA_TEST_URL = 'https://gen.caca01.com/rd/test'

ROOT_PATH = 'dataset/tixcraft'
TEST_PATH = 'test/tixcraft'

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

def collect(loop: int = 1000):
    os.makedirs(ROOT_PATH, exist_ok=True)

    for i in range(loop):
        print(f'{i + 1} / {loop}')
        getQuestData()
        getTestData()


def getMap(files: list[str]) -> Dict[str, PredictInfo]:
    data = {}

    for file in files:
        name = os.path.splitext(file)[0]
        [id, ans] = name.split('_')

        data[file] = PredictInfo(file, ans, '')

    return data

def test():
    ocr = Ocr(ROOT_PATH, TEST_PATH)

    folder_path = Path(ROOT_PATH)
    files = [f.name for f in folder_path.iterdir() if f.is_file()]

    file_map = getMap(files)

    ocr.predict(file_map, 'easyocr')
    ocr.predict(file_map, 'ddddocr')
    ocr.predict(file_map, 'pytesseract')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--collect', action='store_true', help='Run collecting function')
    parser.add_argument('--test', action='store_true', help='Run testing function')

    args = parser.parse_args()

    if args.collect and args.test:
        parser.error("You cannot specify both --collect and --test at the same time.")

    if args.collect:
        collect()
    elif args.test:
        test()
    else:
        parser.error("You must specify either --collect or --test.")
