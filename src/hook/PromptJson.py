import json
import logging
import os

class PromptJson:
    def prompt(self, query, response):
        logging.warning("hihi")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'prompt.json')
        data = {"role": "user", "content": query}
        assistant_data = {"role": "assistant", "content": response}
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                # JSON 파일에서 데이터 읽기
                data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            data_list = []

        data_list.append(data)
        data_list.append(assistant_data)
        logging.warning("dataset", data_list)
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(data_list, outfile, ensure_ascii=False, indent=4)