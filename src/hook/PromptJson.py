import json
import logging
import os




class PromptJson:
    def prompt(self, query, response):
        logging.warning(query)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'prompt.json')
        logging.warning(file_path)
        data = {"role": "user", "content": query}
        assistant_data = {"role": "assistant", "content": response}
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                # JSON 파일에서 데이터 읽기
                data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            # 파일이 없거나 비어있으면 빈 리스트 생성
            data_list = []

        data_list.append(data)
        data_list.append(assistant_data)
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(data_list, outfile, ensure_ascii=False, indent=4)