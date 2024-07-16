import json

path = "./data.JSONL"
def make(cID,tID,text, response):
    query = "채소:"+text
    answer = "SMAF:"+response
    data = {"C_ID":cID,"T_ID":tID,"Text":query,"Completion":answer}

    with open(path, 'a', encoding='utf-8') as outfile:
        outfile.write(json.dumps(data,ensure_ascii=False)+"\n")

