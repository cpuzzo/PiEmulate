# -*- coding: utf-8 -*-
import sys, re
from PyQt4 import QtGui, QtCore
from functools import partial

'''
TODO

1. Add "Are you sure for power down"
2. Add support for users (using PyQt db support?)
'''

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()        
        
        #General use variables        
        self.curr_screen = "home"
        self.prev_screen = ""
        self.systems = {} #manufacturers    
        self.sys_icons = {} #systems icon paths
        self.sys_ems = {} #correlate systems to emulators
        #read text files to fill systems and sys_icons dictionaries        
        self.get_icons()        
        
        #Constants
        self.ASSET_PATH = "C:\\Users\\Christopher\\Documents\\GitHub\\PiEmulate\\assets\\"
        self.EMULATOR_PATH = ""
        self.ROM_PATH = ""
        
        #Set basic properties
        self.setWindowTitle("CeMPulator")
        self.setStyleSheet("background: black; color: silver;")
        self.layout = QtGui.QVBoxLayout(self)  
        
        self.openHomeScreen()
        #self.showFullScreen()
        
    def openHomeScreen(self):
        '''Build home screen containing manufacturer logos'''
      

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
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            grid.addWidget(label,2,i)
            i += 1
            
        self.layout.addLayout(grid)
        
        #instantiate utility row
        self.layout.addLayout(self.buildUtilRow())        
    
    def buildHeader(self, text):
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
        self.prev_screen = "home"
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
  
        i = 0
        row = 0
        for system in systems:
            print('i ' + str(i))
            print('col ' + str(max_col))
            print('row ' + str(row))
            if i == max_col:
                print('here')
                row += 1
                i = 0

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
            grid.addWidget(sys_buttons[-1],row,i)
            
            label = QtGui.QLabel(system)
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            grid.addWidget(label,2,i)
            i += 1
            
        self.layout.addLayout(grid)
        
        self.layout.addLayout(self.buildUtilRow())

    def openSysScreen(self):
        pass
        

    def prevPage(self):
        self.clearLayout(self.layout)
        print(self.prev_screen)
        if self.prev_screen == "home":
            self.openHomeScreen()

    def powerDown(self):
        self.close()      
    
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
        
        #f = open("/home/pi/Desktop/EMpaths")
        txt_path = ("C:\Users\Christopher\Documents\GitHub\PiEmulate\icons.txt")
        curr_mfg = ""
        mfg_sys = []
        f = open(txt_path)
        
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
