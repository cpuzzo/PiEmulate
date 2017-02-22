# -*- coding: utf-8 -*-
import sys, os
from glob import glob
from PyQt5 import QtGui, QtCore, QtWidgets
from functools import partial

'''
TODO
1. Remove need for re package
2. Add support for users (using PyQt db support?)
3. Fix concatenation to use string formatting
4. Add support for minecraft
'''

'''
BUGS
-Back button doesn't work after clicking "no" on shutdown screen
'''


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()        
        
        #General use variables        
        self.curr_screen = "home"
        self.prev_screens = ['']
        self.systems = {} #manufacturers    
        self.sys_icons = {} #systems icon paths
        self.sys_ems = {'nes': 'nestopia'} #correlate systems to emulators        
        
        self.debug = False
        
        #CONSTANTS
        if True == self.debug:
            #WINDOWS
            self.OS_SEP = "\\"
            self.BASE_PATH = "C:\\Users\\Christopher\\Documents\\GitHub\\PiEmulate\\"
            self.TXT_PATH = self.BASE_PATH + r"icons.txt"
        else:
            #LINUX
            self.OS_SEP = "/"
            self.BASE_PATH = "/home/pi/Desktop/PiEmulate/"
            self.TXT_PATH = self.BASE_PATH + r"icons"
    
        self.ASSET_PATH = self.BASE_PATH + "assets" + self.OS_SEP
        self.EMULATOR_PATH = ""
        self.ROM_PATH = ""
                
        #Set basic properties
        self.setWindowTitle("CeMPulator")
        self.setStyleSheet("background: black; color: silver;")
        self.layout = QtWidgets.QVBoxLayout(self)  
        
        #read text files to fill systems and sys_icons dictionaries        
        self.get_icons()                
        
        #open display
        self.openHomeScreen()
        #self.showFullScreen()
        
    def openHomeScreen(self):
        '''Build home screen containing manufacturer logos'''

        self.curr_screen = "home"
        #Instatiate header
        self.layout.addWidget(self.buildHeader("Choose a manufacturer to see available systems:"))
        
        mfg_buttons = []
        
        #create grid of manufacturer buttons        
        grid = QtWidgets.QGridLayout(self)    
        i = 0
        for mfg, systems in self.systems.items():
            icon_path = self.ASSET_PATH + mfg + self.OS_SEP + 'manufacturer.png'
            
            mfg_buttons.append(QtWidgets.QPushButton('',self))
            mfg_buttons[-1].setIcon(QtGui.QIcon(icon_path))
            mfg_buttons[-1].setIconSize(QtCore.QSize(128,128))
            mfg_buttons[-1].clicked.connect(partial(self.openMfgScreen,mfg=mfg, systems=systems))
            grid.addWidget(mfg_buttons[-1],0,i)
            
            label = QtWidgets.QLabel(mfg.capitalize())
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            grid.addWidget(label,2,i)
            i += 1
            
        self.layout.addLayout(grid)
        
        #instantiate utility row
        self.layout.addLayout(self.buildUtilRow())        
    
    def buildHeader(self, text):
        '''Build header message'''
        header = QtWidgets.QLabel(text)
        header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        header.setStyleSheet('font-size: 15em; color: silver;')
        header_font = QtGui.QFont("Times",18,QtGui.QFont.Bold)
        header.setFont(header_font) 
        return header
    
    def buildUtilRow(self):
        '''Build bottom row containing power button and (on any screen other than 'home') a 'back' button'''        
      
        util_row = QtWidgets.QGridLayout(self)
        if self.curr_screen != "home":
            start_col = 1            
            
            back_btn = QtWidgets.QPushButton('',self)
            back_btn.setIcon(QtGui.QIcon(self.ASSET_PATH + "gen" + self.OS_SEP + "back.png"))
            back_btn.setIconSize(QtCore.QSize(64,64))
            back_btn.clicked.connect(self.prevPage)
            util_row.addWidget(back_btn,0,0)
            
        else:
            start_col = 0 
            
        for x in range (start_col,3):
            #create empty grid cells
            space = QtWidgets.QPushButton('',self)
            util_row.addWidget(space,0,x)

        #create power down button
        power_btn = QtWidgets.QPushButton('',self)
        power_btn.setIcon(QtGui.QIcon(self.ASSET_PATH + "gen" + self.OS_SEP +"power.png"))
        power_btn.setIconSize(QtCore.QSize(64,64))
        power_btn.clicked.connect(self.powerDown)
        util_row.addWidget(power_btn,0,4)
     
        return util_row
    
    def openMfgScreen(self, mfg, systems):
        '''Open Manufacturer screen showing available consoles'''
        self.prev_screens = [self.curr_screen] + [self.prev_screens[0]]
        
        self.curr_screen = mfg.lower()
        self.clearLayout(self.layout)
        
        self.layout.addWidget(self.buildHeader("Choose a system to see available games:"))
        
        grid = QtWidgets.QGridLayout(self)
        num_systems = len(systems)
        if num_systems > 4:
            max_col = 4
            rem = num_systems % 4
        elif num_systems % 4 == 0:
            max_col = 4
            rem = None
        elif num_systems % 3 == 0:
            max_col = 3
            rem = None
        elif len(systems) % 2 == 0:
            max_col = 2
            rem = None
        else:
            max_col = 1     
            rem = None

        col = 0
        row = 0
        for system in systems:
            if col == max_col:
                row += 2
                col = 0

                if rem is not None:
                    num_systems += -1
                    if num_systems < 4:
                        max_col = 3

            icon_path = self.ASSET_PATH + mfg + self.OS_SEP + system.lower() + '.png'

            sys_buttons = []                        
            sys_buttons.append(QtWidgets.QPushButton('',self))
            sys_buttons[-1].setIcon(QtGui.QIcon(icon_path))
            sys_buttons[-1].setIconSize(QtCore.QSize(128,128))
            sys_buttons[-1].clicked.connect(partial(self.openSysScreen,mfg=mfg,system=system))
            grid.addWidget(sys_buttons[-1],row,col)

            label = QtWidgets.QLabel(system)
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            grid.addWidget(label,row+1,col)
            col += 1
            
        self.layout.addLayout(grid)
        self.layout.addLayout(self.buildUtilRow())

    def openSysScreen(self, mfg, system):
        self.prev_screens = [self.curr_screen] + [self.prev_screens[0]]
        self.curr_screen = system.lower()
        self.clearLayout(self.layout)
        
        self.layout.addWidget(self.buildHeader("Select Game:"))
        roms = glob(self.ASSET_PATH + mfg + self.OS_SEP + "roms" + self.OS_SEP + "*." + system.lower())

        grid = QtWidgets.QGridLayout(self)
        num_roms = len(roms)
        if num_roms > 4:
            max_col = 4
            rem = num_roms % 4
        if num_roms % 4 == 0:
            max_col = 4
            rem = None
        elif num_roms % 3 == 0:
            max_col = 3
            rem = None
        elif num_roms % 2 == 0:
            max_col = 2
            rem = None
        else:
            pass            
            #self.layout.addWidget(QtWidgets.QPushButton('',self))        
        
        col = 0
        row = 0
        for rom in roms:
            game = rom.split(self.OS_SEP)[-1].split('.')[0]
            ico = self.ASSET_PATH + mfg + self.OS_SEP + "icons" + self.OS_SEP + game + ".png"

            if col == max_col:
                row += 2
                col = 0

                if rem is not None:
                    num_roms += -1
                    if num_roms < 4:
                        max_col = 3

            game_buttons = []            
            game_buttons.append(QtWidgets.QPushButton('',self))
            game_buttons[-1].setIcon(QtGui.QIcon(ico))
            game_buttons[-1].setIconSize(QtCore.QSize(128,128))
            game_buttons[-1].clicked.connect(partial(self.startRom,system=system,rom=rom))
            grid.addWidget(game_buttons[-1],row,col)
            
            label = QtWidgets.QLabel(game)
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            grid.addWidget(label,row+1,col)
            col += 1
            
        self.layout.addLayout(grid)
        self.layout.addLayout(self.buildUtilRow())
         
    def startRom(self, system, rom):
        em_path = self.BASE_PATH + "emulators" + self.OS_SEP + self.sys_ems[system.lower()] 
        
        if True == self.debug:
            os.system("START /MAX " + em_path + " \"" + rom + ".exe\"")            
        else:
            os.system("sudo " + em_path + " \"" + rom + "\"" )

    def prevPage(self):
        self.clearLayout(self.layout)
        
        #if going back to the home screen
        if self.prev_screens[0] == "home":
            self.openHomeScreen()
        
        #if going back to a manufacturer screen
        elif self.prev_screens[0] in self.systems.keys():
            self.openMfgScreen(self.prev_screens[0], self.systems[self.prev_screens[0]])
            
        else:
            pass
            
        self.prev_screens = [self.curr_screen] + [self.prev_screens[0]]

    def powerDown(self):
        self.prev_screens = [self.curr_screen]+[self.prev_screens[0]]        
        self.curr_screen = "power"
        
        self.clearLayout(self.layout)
        self.layout.addWidget(self.buildHeader("Are you sure you would like to shut down?"))
        
        choice_row = QtWidgets.QGridLayout(self)    
        #create NO button        
        no_btn = QtWidgets.QPushButton('',self)
        no_btn.setIcon(QtGui.QIcon(self.ASSET_PATH + "gen" +self.OS_SEP + "no.png"))
        no_btn.setIconSize(QtCore.QSize(64,64))
        no_btn.clicked.connect(partial(self.shutdownUserChoice,choice=False))
        choice_row.addWidget(no_btn,0,0)
        
        #create YES button
        yes_btn = QtWidgets.QPushButton('',self)
        yes_btn.setIcon(QtGui.QIcon(self.ASSET_PATH + "gen" +self.OS_SEP + "confirm.png"))
        yes_btn.setIconSize(QtCore.QSize(64,64))
        yes_btn.clicked.connect(partial(self.shutdownUserChoice,choice=True))
        choice_row.addWidget(yes_btn,0,1)   
        
        self.layout.addLayout(choice_row)
            
    def shutdownUserChoice(self, choice):
        if True == choice:
            self.close()     
            #os.system('shutdown now -h')
        else:
            self.prevPage()
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
        
    def get_icons(self):
        '''fetch manufacturer and system information from logfile'''
        curr_mfg = ""
        mfg_sys = []
        f = open(self.TXT_PATH)
        
        for line in f.readlines():
            if line[0] == "#":
                next
            elif '~' in line:
                mfg_sys=[]
                curr_mfg = line.split('~')[1]
                if curr_mfg != "":
                    self.systems[curr_mfg] = mfg_sys
            else:
                system = line.strip() #get system name without newline
                mfg_sys.append(system)
                self.sys_icons[system] = line
                
        f.close()
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()
