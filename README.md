# spellCheck  
championDF.py : makes 1)champion.jpg, 2)champion.csv 
runeDF.py : makes 1) rune.csv  
spellDF.py : makes 1) spell.jpg, 2) spell.csv  
  
spellCheckGUIv.2.py : uses PyQt5  
spellCheckchg.py : has functions for 'spellCheckGUIv.1.py'.  

## HOW TO USE  
1. get lol api key on https://developer.riotgames.com/  
2. open the file "SpellCheck.exe"  
* it is slow because it is made by pyinstaller -> no console mode
  
![image](https://github.com/DeckofKard/spellCheck/assets/113531187/c6ecea32-db97-4ca1-8d4f-37d8677bd448)

3. enter the api key and your Ingmae nickname(only available in KOR server), press 'login'
* if the program quit unexpectadly, it may be problem of your
    1) api key (ctrl+v it well)
    2) nick name (without spacing)
    3) you are not playing it right now (because it can only get current ingame data)
  
![image](https://github.com/DeckofKard/spellCheck/assets/113531187/70235f6e-9aab-4a5d-ac1d-ae994734a4fb)
  
4. edit your ingame playtime if the time on program is not right
5. push the spell button to calculate spell cooltime based on rune(Cosmic Insight), Ionian Boots.
6. the messages on the program is updated when you push any spell button, not automatically.
   
https://blog.naver.com/qww9363/223143947574
