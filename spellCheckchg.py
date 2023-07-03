# for spellCheckGUIv.1
# does actual data settings for GUI
import requests
import pandas as pd
from datetime import datetime
# import json

class spellcheck:
    def getApikey(api_key):              # api_key -> request_header
        request_header = {                                          # for api request header
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,es;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": api_key
        }
        return request_header
    
    def getName(name):      # returns string(Ingame user nickname)
        return name

    def setUIforspellcheck(name, request_header):   # returns puuid of user
        CodeDF = pd.read_csv("csv_file\\champion.csv")      # columns : 'name', 'code'
        

        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"
        AccountData = requests.get(url, headers=request_header).json()
        temp_id = AccountData['id']

        url = f"https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{temp_id}"
        CurrentGame = requests.get(url, headers=request_header).json()

        # if you want to check the structure of currentgame by json file, try this.
        
        #with open("json_file\\currentgame2.json", "w", encoding='utf-8') as f:         
        #    json.dump(CurrentGame, f)

        Users = CurrentGame['participants']

        teamId = []                             # int
        name = []                               # string
        champ = []                              # int(code.ver)
        CosmicInsightBool = []                  # bool
        spell1 = []                             # int
        spell2 = []                             # int
        IonianBootsOfLucidity = []              # bool

        for user in Users:
            teamId.append(user['teamId'])
            if user['summonerName'] == AccountData['name']:                                 # user team config
                playerTeam = user['teamId']
            
            name.append(user['summonerName'])                                               # user summonerName

            name_ = CodeDF.loc[CodeDF['code'] == user['championId'], 'name'].iloc[0]        # user champion name
            champ.append(name_)       

            perk = user['perks']['perkIds']                                                 # Cosmic Insight config
            if 8347 in perk:
                CosmicInsightBool.append(True)
            else:
                CosmicInsightBool.append(False)

            spell1.append(str(user['spell1Id']) + '_' + name_)                              # spell config(1, 2)
            spell2.append(str(user['spell2Id']) + '_' + name_)                              # ex. 14_Hideonbush

            IonianBootsOfLucidity.append(False)
            
        CurrentGameDF = pd.DataFrame({'teamId' : teamId,                                    # lists to dataframe 
                                    'name' : name,
                                    'champ' : champ,
                                    'CosmicInsight' : CosmicInsightBool,
                                    'spell1' : spell1,
                                    'spell2': spell2,
                                    'IonianBoots' : IonianBootsOfLucidity})  
    
        CurrentGameDF.drop(CurrentGameDF[(CurrentGameDF['teamId']==playerTeam)].index, inplace=True)        # drop our team
                                                                                                            # don`t need our teams info.

        now = datetime.now()
        StartTime = int(now.timestamp() * 1000)                         # convert now to milsec(int)
        StartTime -= (CurrentGame['gameLength']*1000)                   # start time : when the users are on the rift

        return CurrentGameDF, StartTime

    def ChampionJPG(championCode):                                      # returns the path of {champion}.jpg          
        return f"jpg_file\\{championCode}.jpg"

    def SpellJPG(spellCode):                                            # returns the path of {spell}.jpg         
        return f"jpg_file\\{spellCode}.jpg"



# this class is for calculation of spell.
# the times are converted to millisec(10^-3 second)
class CoolCheck:                
    def CalCulateCoolbyformula(stat, cooltime):                                         # formula to calculate spell by the stat, cooltime reduction
        cooltime = round(cooltime/1000)
        return round(cooltime * 100 / (100 + stat)) * 1000

    # cooltime = cooltime * {100 / (100 + cosmicInsight(18) or IonianBoots(12))}    
    # when both cosmicInsight and IonianBoots exists, it is calculated seperately
    # then calculated as 'sum operation'
    def CoolTimeCalculate(IonianBoots, CosmicInsight, spellCode):                       # returns calculated CoolTime as milsec                                                                           
        SpellDF = pd.read_csv("csv_file\\spell.csv", encoding='utf-8')                  # columns : 'name', 'key', 'img_path', 'cooltime'

        CoolTime_ = SpellDF.loc[SpellDF['key'] == spellCode, 'cooltime'].iloc[0]        # convert to mil sec
        CoolTime_ = int(CoolTime_) * 1000

        spellName = SpellDF.loc[SpellDF['key'] == spellCode, 'name'].iloc[0]            # string(ex. Flash)

        IonianBoots_ = CoolCheck.CalCulateCoolbyformula(12, CoolTime_)                  # IonianBoots : 12
        CosmicInsight_ = CoolCheck.CalCulateCoolbyformula(18, CoolTime_)                # CosmicInsight : 18

        if IonianBoots == True and CosmicInsight == True:                               # True True
            CoolTime = IonianBoots_ + CosmicInsight_ - CoolTime_
        elif IonianBoots == True and CosmicInsight == False:                            # True False
            CoolTime = IonianBoots_
        elif IonianBoots == False and CosmicInsight == True:                            # False True    
            CoolTime = CosmicInsight_
        else:                                                                           # False False
            CoolTime = CoolTime_
        
        return CoolTime, spellName

    def CoolTime(Cooltime, startTime):                          # returns Cooltime_(int)
        now_ = datetime.now()
        now = int(now_.timestamp() * 1000)                      # convert now to milsec(int) 
        Cooltime_ = (now - startTime) + Cooltime
        return Cooltime_, now

    
    def DelWhenCoolOver(checkSpellDF, startTime):                   # returns dataframe(the fixed checkSpellDF)
        now_ = datetime.now()
        now = int(now_.timestamp() * 1000)                          # convert now to milsec(int) 
        IngameTime = now - startTime
        checkSpellDF.drop(checkSpellDF[(checkSpellDF['cooltime']) <= IngameTime].index, inplace=True)   # deletes string(s) of checklist when the cool is over
        print(checkSpellDF)
        checkSpellDF = CoolCheck.DelDuplicateChampName(checkSpellDF)
        print(checkSpellDF)
        return checkSpellDF
    
    def DelDuplicateChampName(checkSpellDF):            # drops Duplicate champ name & spell 
        checkSpellDF = checkSpellDF.sort_values('when').drop_duplicates(['spellName', 'champ'], keep = 'last').sort_index()
        return checkSpellDF
    
#-*- coding: utf-8 -*-