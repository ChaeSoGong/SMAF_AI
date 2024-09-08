import json
import logging
import os


class PromptJson:
    @staticmethod
    def prompt(f_or_t, query, response):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if f_or_t == 0:
            file_path = os.path.join(base_dir, 'prompt.json')
        else:
            file_path = os.path.join(base_dir, 't_prompt.json')
        if query == "no":
            data = None
        else:
            data = {"role": "user", "content": query}
        assistant_data = {"role": "assistant", "content": response}
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            data_list = []

        if data is not None:
            data_list.append(data)
        data_list.append(assistant_data)
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(data_list, outfile, ensure_ascii=False, indent=4)