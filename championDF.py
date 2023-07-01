import urllib.request
import json
import pandas as pd
'''
it downloads champion name, code number, and png of the champion

png is downloaded to jpg_file\\{championName}.png
name and code number is downloaded to csv_file\\champion.csv
'''
championName = []
championCode = []

with open("json_file\\champion.json", "rt", encoding='utf-8') as file:
    championJson_ = json.load(file)
    for championName_ in championJson_['data']:
        championName.append(championJson_['data'][championName_]['id'])

    for championName_ in championName:
        key = championJson_["data"][championName_]["key"]
        championCode.append(key)

        url = f"http://ddragon.leagueoflegends.com/cdn/13.13.1/img/champion/{championName_}.png"
        urllib.request.urlretrieve(url, f"jpg_file\\{championName_}.jpg")

    df = pd.DataFrame({'name' : championName,
                       'code' : championCode})
    df.to_csv("csv_file\\champion.csv")
