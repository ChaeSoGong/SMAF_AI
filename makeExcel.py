# excel
import csv
import pandas as pd

def excel(cID,tID,text,response):
    f = open('smaf.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    c_ID = cID
    t_ID = tID
    t = "채소:"+text
    r = "SMAF:"+response
    wr.writerow([c_ID,t_ID,t,r])
    f.close()

