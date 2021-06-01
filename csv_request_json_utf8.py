import csv
import json
import requests

url = 'http://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTocupestacbici/ocupestacbici.csv'
headers = {'User-Agent': 'myagent'}
response=requests.get(url,headers=headers)
response.encoding='utf-8'
reader = csv.reader(response.text.splitlines(),delimiter=',')
header_row = next(reader)

for row in reader:
    print(row[1])
    print(row)
    '''
    data={
        'id': row[0],
        'libres': row[7]
    }
    json_data=json.dumps(data)
    
    print(json_data)
    '''