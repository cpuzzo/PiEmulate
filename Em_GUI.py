# -*- coding: utf-8 -*-
import sys, re, os
from glob import glob
from PyQt4 import QtGui, QtCore
from functools import partial

'''
TODO
1. Remove need for re package
2. Add support for users (using PyQt db support?)
'''

'''
BUGS
-Back button doesn't work after clicking "no" on shutdown screen
'''

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()        
        
        #General use variables        
        self.curr_screen = "home"
        self.prev_screens = ['']
        self.systems = {} #manufacturers    
        self.sys_icons = {} #systems icon paths
        self.sys_ems = {} #correlate systems to emulators
                
        #Constants
        self.BASE_PATH = "C:\\Users\\cpuzzo\\Documents\\GitHub\\PiEmulate\\"
        #self.ASSET_PATH = "C:\\Users\\Christopher\\Documents\\GitHub\\PiEmulate\\assets\\"
        self.ASSET_PATH = self.BASE_PATH + "assets\\"
        self.EMULATOR_PATH = ""
        self.ROM_PATH = ""
        
        #self.TXT_PATH r"/home/pi/Desktop/EMpaths"
        #self.TXT_PATH = r"C:\Users\Christopher\Documents\GitHub\PiEmulate\icons.txt"
        self.TXT_PATH = self.BASE_PATH + r"icons.txt"
        
        #Set basic properties
        self.setWindowTitle("CeMPulator")
        self.setStyleSheet("background: black; color: silver;")
        self.layout = QtGui.QVBoxLayout(self)  
        
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
        grid = QtGui.QGridLayout(self)    
        i = 0
        for mfg, systems in self.systems.items():
            icon_path = self.ASSET_PATH + mfg + '\\manufacturer.png'
            
            mfg_buttons.append(QtGui.QPushButton('',self))
            mfg_buttons[-1].setIcon(QtGui.QIcon(icon_path))
            mfg_buttons[-1].setIconSize(QtCore.QSize(128,128))
            mfg_buttons[-1].clicked.connect(partial(self.openMfgScreen,mfg=mfg, systems=systems))
            grid.addWidget(mfg_buttons[-1],0,i)
            
            label = QtGui.QLabel(mfg.capitalize())
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            grid.addWidget(label,2,i)
            i += 1
            
        self.layout.addLayout(grid)
        
        #instantiate utility row
        self.layout.addLayout(self.buildUtilRow())        
    
    def buildHeader(self, text):
        '''Build header message'''
        header = QtGui.QLabel(text)
        header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        header.setStyleSheet('font-size: 15em; color: silver;')
        header_font = QtGui.QFont("Times",18,QtGui.QFont.Bold)
        header.setFont(header_font) 
        return header
    
    def buildUtilRow(self):
        '''Build bottom row containing power button and (on any screen other than 'home') a 'back' button'''        
      
        util_row = QtGui.QGridLayout(self)
        if self.curr_screen != "home":
            start_col = 1            
            
            back_btn = QtGui.QPushButton('',self)
            back_btn.setIcon(QtGui.QIcon(self.ASSET_PATH + "gen\\back.png"))
            back_btn.setIconSize(QtCore.QSize(64,64))
            back_btn.clicked.connect(self.prevPage)
            util_row.addWidget(back_btn,0,0)
            
        else:
            start_col = 0 
            
        for x in range (start_col,3):
            #create empty grid cells
            space = QtGui.QPushButton('',self)
            util_row.addWidget(space,0,x)

        #create power down button
        power_btn = QtGui.QPushButton('',self)
        power_btn.setIcon(QtGui.QIcon(self.ASSET_PATH + "gen\\power.png"))
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
        
        grid = QtGui.QGridLayout(self)
        num_systems = len(systems)
        if num_systems > 4:
            max_col = 4
            rem = num_systems % 4
        if num_systems % 4 == 0:
            max_col = 4
            rem = None
        elif num_systems % 3 == 0:
            max_col = 3
            rem = None
        elif len(systems) % 2 == 0:
            max_col = 2
            rem = None
        else:
            pass            
            #self.layout.addWidget(QtGui.QPushButton('',self))
  
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
                
            icon_path = self.ASSET_PATH + mfg + '\\' + system.lower() + '.png'
            sys_buttons = []            
            
            sys_buttons.append(QtGui.QPushButton('',self))
            sys_buttons[-1].setIcon(QtGui.QIcon(icon_path))
            sys_buttons[-1].setIconSize(QtCore.QSize(128,128))
            sys_buttons[-1].clicked.connect(partial(self.openSysScreen,system=system))
            grid.addWidget(sys_buttons[-1],row,col)
            
            label = QtGui.QLabel(system)
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            grid.addWidget(label,row+1,col)
            col += 1
            
        self.layout.addLayout(grid)
        self.layout.addLayout(self.buildUtilRow())

    def openSysScreen(self, system):
        pass
        
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
            
        self.prev_screens = [self.curr_screen] + [self.prev_screen[0]]

    def powerDown(self):
        self.prev_screens = [self.curr_screen]+[self.prev_screens[0]]        
        self.curr_screen = "power"
        
        self.clearLayout(self.layout)
        self.layout.addWidget(self.buildHeader("Are you sure you would like to shut down?"))
        
        choice_row = QtGui.QGridLayout(self)    
        #create NO button        
        no_btn = QtGui.QPushButton('',self)
        no_btn.setIcon(QtGui.QIcon(self.ASSET_PATH + "gen\\no.png"))
        no_btn.setIconSize(QtCore.QSize(64,64))
        no_btn.clicked.connect(partial(self.shutdownUserChoice,choice=False))
        choice_row.addWidget(no_btn,0,0)
        
        #create YES button
        yes_btn = QtGui.QPushButton('',self)
        yes_btn.setIcon(QtGui.QIcon(self.ASSET_PATH + "gen\\confirm.png"))
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
            if '~' in line:
                mfg_sys=[]
                curr_mfg = re.split('~',line)[1]
                if curr_mfg != "":
                    self.systems[curr_mfg] = mfg_sys
            else:
                system = re.split(r"\\",line)[-1][:-1:] #get system name without newline
                mfg_sys.append(system)
                self.sys_icons[system] = line
                
        f.close()
        return

def main():
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()
