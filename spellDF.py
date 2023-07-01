# how to get png?
# http://ddragon.leagueoflegends.com/cdn/13.13.1/img/spell/{__}.png
# needs Spelljson_ -> data -> <spell name> -> image -> full
import urllib.request
import json
import pandas as pd

with open("json_file\\summoner.json", "rt", encoding='utf-8') as file:      # json file of spells
    Spelljson_ = json.load(file)
    spellData = []
    for data_ in Spelljson_['data']:
        spellData.append(data_)

    name = []
    key = []
    img_path = []
    cooltime = []
    for data_ in spellData:
        name.append(Spelljson_['data'][data_]['name'])
        key.append(Spelljson_['data'][data_]['key'])
        img_path.append(Spelljson_['data'][data_]['image']['full'])
        cooltime.append(int(Spelljson_['data'][data_]['cooldownBurn']))
        url = f"http://ddragon.leagueoflegends.com/cdn/13.13.1/img/spell/{Spelljson_['data'][data_]['image']['full']}"
        urllib.request.urlretrieve(url, f"jpg_file\\{Spelljson_['data'][data_]['key']}.jpg")

    df = pd.DataFrame({'name': name,
                       'key': key,
                       'img_path':img_path,
                       'cooltime':cooltime})
    df.to_csv("csv_file\\spell.csv")
    
    

    