import json
import pandas as pd
with open("json_file\\runesReforged.json", 'r', encoding='utf-8') as f:
    runeData = json.load(f)
runeId = []
runeName = []
for rune in runeData:
    for Def in rune['slots']:
        for rune_ in Def['runes']:
            runeId.append(rune_['id'])
            runeName.append(rune_['key'])
df = pd.DataFrame(zip(runeId, runeName))
df.to_csv('rune.csv')          