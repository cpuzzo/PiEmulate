# -*- coding: utf-8 -*-
import sys, re
from PyQt4 import QtGui, QtCore
from functools import partial

'''
TODO

1. Set grid with messages and power/back button row 
2. Add true Icon buttons
3. Add support for users (using PyQt db support?)
4. Formatting
'''

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("CeMPulator")
        layout = QtGui.QVBoxLayout(self)        
        self.setStyleSheet("background: black; color: silver;")
        
        header = QtGui.QLabel("Choose a manufacturer to see available systems:")
        header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        header.setStyleSheet('font-size: 15em; color: silver;')
        header_font = QtGui.QFont("Times",18,QtGui.QFont.Bold)
        header.setFont(header_font) 
        layout.addWidget(header)
        
        self.systems = {} #manufacturers    
        self.sys_icons = {} #systems icon paths
        
        self.mfg_icon_basepath = "C:\\Users\\Christopher\\Documents\\GitHub\\PiEmulate\\assets\\"
        #self.showFullScreen()
        
        self.get_icons()
        self.buttons = []
        i = 0
        
        grid = QtGui.QGridLayout(self)    
                
        for mfg, systems in self.systems.items():
            icon_path = self.mfg_icon_basepath + mfg + '\\manufacturer.png'
            self.buttons.append(QtGui.QPushButton('',self))
            self.buttons[-1].setIcon(QtGui.QIcon(icon_path))
            self.buttons[-1].setIconSize(QtCore.QSize(128,128))
            self.buttons[-1].clicked.connect(partial(self.handleButton,data=systems))
            grid.addWidget(self.buttons[-1],0,i)
            
            label = QtGui.QLabel(mfg.capitalize())
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            grid.addWidget(label,2,i)
            i += 1
        layout.addLayout(grid)
        
        util_row = QtGui.QGridLayout(self)
        back_btn = QtGui.QPushButton('',self)
        back_btn.setIcon(QtGui.QIcon(self.mfg_icon_basepath + "gen\\back.png"))
        back_btn.setIconSize(QtCore.QSize(64,64))
        back_btn.clicked.connect(self.prevPage)
        util_row.addWidget(back_btn,0,0)
        
        for x in range (1,3):
            space = QtGui.QPushButton('',self)
            util_row.addWidget(space,0,x)
        
        power_btn = QtGui.QPushButton('',self)
        power_btn.setIcon(QtGui.QIcon(self.mfg_icon_basepath + "gen\\power.png"))
        power_btn.setIconSize(QtCore.QSize(64,64))
        power_btn.clicked.connect(self.powerDown)
        util_row.addWidget(power_btn,0,4)
        layout.addLayout(util_row)
        
    def prevPage(self):
        pass

    def powerDown(self):
        pass        

        
    def handleButton(self, data='\n'):
        print(data)
        
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
