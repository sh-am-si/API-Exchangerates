import csv
import json
import requests

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

data_from_json = json.loads(json.dumps(data))

rates = {}

def get_rates():
    for data in data_from_json:
        rates = data['rates']    

    with open('exchangerates.csv', 'w', newline='') as csvfile:
        fieldnames = ['currency', 'code', 'bid', 'ask']
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for rate in rates:          
            writer.writerow({'currency': rate["currency"], 'code': rate["code"], 'bid': rate["bid"], 'ask': rate["ask"]})

get_rates()
