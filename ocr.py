import os
import csv
from typing import Dict

import easyocr

row_label = ['檔案名稱', '正確答案', '預測答案']

class PredictInfo:
    def __init__(self, file: str, ans: str, result: str):
        self.file = file
        self.ans = ans
        self.result = result

    def to_dict(self):
        return {row_label[0]: self.file, row_label[1]: self.ans, row_label[2]: self.result}

class Ocr:
    def __init__(self, data_path: str, result_path: str):
        self.data_path = data_path
        self.result_path = result_path

        self.easyocr_reader = easyocr.Reader(['en'])

        os.makedirs(result_path, exist_ok=True)

    def predict(self, predictInfo: Dict[str, PredictInfo], model: str):
        data = []

        correct = 0
        cnt = 0

        for key in predictInfo:
            file_path = f'{self.data_path}/{file_info.file}'

            file_info = predictInfo[key]
            prediect_ans = ''

            if file_info.result == '':
                if model == 'easyocr':
                    result = self.easyocr_reader.readtext(file_path, detail = 0)
                    prediect_ans = result[0].lower()
                else:
                    raise Exception('Not support model')

            file_info.result = prediect_ans

            data.append(file_info.to_dict())

            if file_info.result == file_info.ans:
                correct += 1
            cnt += 1

            status = f'Precision: {correct / cnt:.2f} ({correct} / {cnt})'
            print(status, end='\r')

            txt_filename = f'{self.result_path}/{model}.txt'
            with open(txt_filename, mode='w', newline='', encoding='utf-8') as file:
                file.write(status)

            csv_filename = f'{self.result_path}/{model}.csv'
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=row_label)

                writer.writeheader()
                writer.writerows(data)

            result = self.easyocr_reader.readtext(file_path, detail = 0)
            file_info.result = result[0].lower()
