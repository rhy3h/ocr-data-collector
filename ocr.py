import os
import csv
from typing import Dict

import easyocr
import ddddocr

row_label = ['File', 'Answer', 'Predict']

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

        self.ddddocr = ddddocr.DdddOcr(show_ad=False)
        self.ddddocr.set_ranges(1)

        os.makedirs(result_path, exist_ok=True)

    def predict(self, predictInfo: Dict[str, PredictInfo], model: str):
        txt_filename = f'{self.result_path}/{model}.txt'
        csv_filename = f'{self.result_path}/{model}.csv'

        data = []

        correct = 0
        cnt = 0

        for key in predictInfo:
            file_info = predictInfo[key]

            file_path = f'{self.data_path}/{file_info.file}'

            prediect_ans = ''

            if file_info.result == '':
                if model == 'easyocr':
                    result = self.easyocr_reader.readtext(file_path, detail = 0)
                    try:
                        prediect_ans = result[0].lower()
                    except:
                        pass
                elif model == 'ddddocr':
                    image = open(file_path, 'rb').read()
                    result = self.ddddocr.classification(image)
                    prediect_ans = result
                else:
                    raise Exception('Not support model')

            file_info.result = prediect_ans

            data.append(file_info.to_dict())

            if file_info.result == file_info.ans:
                correct += 1
            cnt += 1

            status = f'Precision: {correct / cnt:.2f} ({correct} / {cnt})'
            print(status, end='\r')

            with open(txt_filename, mode='w', newline='', encoding='utf-8') as file:
                file.write(status)

            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=row_label)

                writer.writeheader()
                writer.writerows(data)
