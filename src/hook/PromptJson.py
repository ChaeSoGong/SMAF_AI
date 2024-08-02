import json

path = "../prompt.json"

class PromptJson:
    def prompt(self, query, response):
        data = {"role": "user", "content": query}
        assistant_data = {"role": "assistant", "content": response}
        try:
            with open(path, 'r', encoding='utf-8') as infile:
                # JSON 파일에서 데이터 읽기
                data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            # 파일이 없거나 비어있으면 빈 리스트 생성
            data_list = []

        data_list.append(data)
        data_list.append(assistant_data)
        with open(path, 'w', encoding='utf-8') as outfile:
            json.dump(data_list, outfile, ensure_ascii=False, indent=4)