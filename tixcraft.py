import argparse
import json
import base64
import os
import csv

from typing import Dict

import requests
from pathlib import Path

from ocr import Ocr

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

def collect(loop: int = 100):
    os.makedirs(ROOT_PATH, exist_ok=True)

    for i in range(loop):
        print(f'{i + 1} / {loop}')
        getQuestData()
        getTestData()

row_label = ['檔案名稱', '正確答案', '預測答案']

class PredictInfo:
    def __init__(self, file: str, ans: str, result: str):
        self.file = file
        self.ans = ans
        self.result = result

    def to_dict(self):
        return {row_label[0]: self.file, row_label[1]: self.ans, row_label[2]: self.result}

def getMap(files: list[str]) -> Dict[str, PredictInfo]:
    data = {}

    for file in files:
        name = os.path.splitext(file)[0]
        [id, ans] = name.split('_')

        data[file] = PredictInfo(file, ans, '')

    return data

def test():
    os.makedirs(TEST_PATH, exist_ok=True)

    ocr = Ocr()

    folder_path = Path(ROOT_PATH)
    files = [f.name for f in folder_path.iterdir() if f.is_file()]

    correct = 0
    cnt = 0

    data = []

    file_map = getMap(files)

    for key in file_map:
        file_info = file_map[key]

        file_path = f'{ROOT_PATH}/{file_info.file}'

        if file_info.result == '':
            result = ocr.predictByEasyOcr(file_path)
            file_info.result = result[0].lower()

        data.append(file_info.to_dict())

        if file_info.result == file_info.ans:
            correct += 1
        cnt += 1

        status = f'Precision: {correct / cnt:.2f} ({correct} / {cnt})'
        print(status, end='\r')

        txt_filename = f'{TEST_PATH}/easyocr.txt'
        with open(txt_filename, mode='w', newline='', encoding='utf-8') as file:
            file.write(status)

        csv_filename = f'{TEST_PATH}/easyocr.csv'
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=row_label)

            writer.writeheader()
            writer.writerows(data)

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
        parser.error("You must specify either --train or --test.")
