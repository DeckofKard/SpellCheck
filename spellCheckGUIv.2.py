# can change the current Ingame time by 'edit'
# when the program starts, the current ingame time is gotten by currentgame.json in lol.api in spellCheckchg.py
# but the time is not correct, so you can change it by your own

import sys
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMainWindow, QWidget, QVBoxLayout, QLabel, QToolButton, QHBoxLayout, QCheckBox, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import pandas as pd
import spellCheckchg
from datetime import datetime
# import clipboard

name = None
request_header = None

class checkIds(QDialog):     # gets apikey and request header
    def __init__(self):
        super().__init__()
        self.init_Data()

    def init_Data(self):         # apikey, name input
        self.api_key_input = None
        self.name_input = None

        main_layout = QFormLayout()         # set layout

        self.api_key_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        login_button = QPushButton("login", self)

        main_layout.addRow("API KEY : ", self.api_key_input)
        main_layout.addRow("NAME : ", self.name_input)
        main_layout.addRow("", login_button)

        self.setLayout(main_layout)
        self.resize(300,100)
        self.show()

        login_button.clicked.connect(self.toInGame)     # get the data

    
    def toInGame(self):         # returns data(api_key -> request_header, name) to <class : InGame>
        #if self.api_key_input is not None or self.name_input is not None:
        #    return
        
        request_header = spellCheckchg.spellcheck.getApikey(self.api_key_input.text())
        name = spellCheckchg.spellcheck.getName(self.name_input.text())

        self.hide()
        Ingame = InGame(request_header, name, self)
        Ingame.show()


class InGame(QMainWindow):                  # actual game UI of opponents
    def __init__(self, request_header, name, parent=None):
        super().__init__(parent)
        self.request_header = request_header
        self.name = name

        self.resize(250,300)
        self.GameData()

        self.checkSpellDF = pd.DataFrame()            # writes spell check time
        self.checkSpellDF['champ'] = ''
        self.checkSpellDF['spellName'] = ''
        self.checkSpellDF['cooltime'] = ''
        self.checkSpellDF['when'] = ''

    def GameData(self):                                 # UI of opponents {champion, spell_1, spell_2} 
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # gets game dataframe, start time, current length
        self.CurrentGameDF, self.startTime = spellCheckchg.spellcheck.setUIforspellcheck(self.name, self.request_header)                

        line_row_set = []
        for index, user in self.CurrentGameDF.iterrows():
            line_set = []

            name = spellCheckchg.spellcheck.ChampionJPG(user['champ'])
            pixmap = QPixmap(name).scaledToHeight(50)
            label = QLabel()
            label.setPixmap(pixmap)

            temp = user['spell1'].find('_')
            spell1_ = user['spell1'][:temp]

            temp = user['spell2'].find('_')
            spell2_ = user['spell2'][:temp]


            # spell 1 button
            spell1 = spellCheckchg.spellcheck.SpellJPG(spell1_)
            pixmap = QPixmap(spell1).scaledToHeight(50)
            spell1_button = QToolButton()
            spell1_button.setText('')
            spell1_button.setProperty("button_id", user['spell1'])
            spell1_button.setIcon(QIcon(pixmap))
            spell1_button.setIconSize(pixmap.size())
            spell1_button.clicked.connect(self.checkCooltime)

            # spell 2 button
            spell2 = spellCheckchg.spellcheck.SpellJPG(spell2_)
            pixmap = QPixmap(spell2).scaledToHeight(50)
            spell2_button = QToolButton()
            spell2_button.setText('')
            spell2_button.setProperty("button_id", user['spell2'])
            spell2_button.setIcon(QIcon(pixmap))
            spell2_button.setIconSize(pixmap.size())
            spell2_button.clicked.connect(self.checkCooltime)

            # IonianBoots
            IonianBoots = QCheckBox("IonianBoots", self)
            IonianBoots.setProperty("checkbox", user['name'])
            IonianBoots.stateChanged.connect(self.IonianBootsState)


            line_set.append(label)
            line_set.append(spell1_button)
            line_set.append(spell2_button)
            line_set.append(IonianBoots)

            line_row_set.append(line_set)

        

        for line_set in line_row_set:
            line_layout = QHBoxLayout()
            for widget in line_set:
                line_layout.addWidget(widget)
            layout.addLayout(line_layout)

        # where the full message is on
        self.Result = QLabel()
        layout.addWidget(self.Result)

        # for time reset
        edit = QHBoxLayout()
        self.EditTime = QToolButton()
        self.EditTime.setText("Edit Time")
        edit.addWidget(self.EditTime)
        self.EditTImeEdit = QLineEdit()
        edit.addWidget(self.EditTImeEdit)
        layout.addLayout(edit)
        self.EditTime.clicked.connect(self.setTime)

        self.show()
    def setTime(self):
        time_ = self.EditTImeEdit.text() 
        time_ = time_.replace(" ", "")      # null destroy
        now = datetime.now()
        StartTime = int(now.timestamp() * 1000)
        print(time_)
        if ':' in time_:
            min_ = int(time_[ : time_.find(':')])
            sec_ = int(time_[time_.find(':') + 1 : ])
            print(min_, sec_)
            self.startTime = StartTime - (min_ * 60 + sec_) * 1000
        else:
            self.startTime = StartTime - 1 * 60 * 1000          # default : 1:00 start app

        return


    def checkCooltime(self):
        sender = self.sender()
        buttonData = sender.property("button_id")                   # buttonData : ex. 4_Azir (-> flash, Azir)

        spellCode = int(buttonData[:buttonData.find('_')])          # values to calculate with
        champName = buttonData[buttonData.find('_')+1:]
        IonianBoots = self.CurrentGameDF.loc[self.CurrentGameDF['champ'] == champName, 'IonianBoots'].iloc[0]
        CosmicInsight = self.CurrentGameDF.loc[self.CurrentGameDF['champ'] == champName, 'CosmicInsight'].iloc[0] 

        Cooltime, spellName = spellCheckchg.CoolCheck.CoolTimeCalculate(IonianBoots, CosmicInsight, spellCode)

        
        CooltimeInGame, now_ = spellCheckchg.CoolCheck.CoolTime(Cooltime, self.startTime)

        CoolRow = {'champ' : champName, 'spellName' : spellName, 'cooltime' : CooltimeInGame, 'when' : now_}

        self.checkSpellDF = pd.concat([self.checkSpellDF, pd.DataFrame([CoolRow])], ignore_index=True)

        self.checkSpellDF = spellCheckchg.CoolCheck.DelWhenCoolOver(self.checkSpellDF, self.startTime)    # check cooltime
        InGame.msg(self)
        
        coolTime_ = divmod(round(Cooltime/1000), 60)
        sender.setText(f"{coolTime_[0]}:{coolTime_[1]}")
        
        return 
    
    def IonianBootsState(self, state):
        sender = self.sender()
        userName = sender.property("checkbox")
        if state == Qt.CheckState.Checked:
            self.CurrentGameDF.loc[self.CurrentGameDF['name'] == userName, "IonianBoots"] = True
        else:
            self.CurrentGameDF.loc[self.CurrentGameDF['name'] == userName, "IonianBoots"] = False
        return
    
    def msg(self):          # copies msg to clipboard -> can use in game on chat by ctrl+v
        # checked on 01.07.2023
        # in lol Ingame, can not copy msg on chat(denied)
        # so, made 'show' for use
        msg_ = ''
        for champName in self.checkSpellDF['champ'].unique():
            filtered_rows = self.checkSpellDF[self.checkSpellDF['champ'] == champName]
            msg_ += champName
            for index, row in filtered_rows.iterrows():
                spellName = row['spellName']
                coolTime = row['cooltime']

                coolTime_ = divmod(round(coolTime/1000), 60)
                msg_ += f" {spellName} {coolTime_[0]}:{coolTime_[1]} "
            msg_ += '\n'
        # clipboard.copy(msg_)      // can`t be used Ingame
        self.showMsg(msg_)
        return
    
    def showMsg(self, msg_):
        # shows msg under the UI of champ & spell
        # tells the user when the spell is going to be 'on'
        self.Result.setText(msg_)
        return


if __name__ == '__main__':              # main
    app = QApplication(sys.argv)
    window = checkIds()
    sys.exit(app.exec_())
#-*- coding: utf-8 -*-