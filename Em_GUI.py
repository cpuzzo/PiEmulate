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
        layout = QtGui.QGridLayout(self)
        self.setStyleSheet("background: black; color: silver;")
        #layout.addLayout(QtGui.QHBoxLayout,0,0)
        
        self.systems = {} #manufacturers    
        self.sys_icons = {} #systems icon paths
        
        self.mfg_icon_basepath = "C:\\Users\\Christopher\\Documents\\GitHub\\PiEmulate\\assets\\"
        #self.showFullScreen()
        
        #Initiate buttons
        #back = QtGui.QPushButton(self)
        #power = QtGui.QPushButton(self)
        
        self.get_icons()
        self.buttons = []
        i = 0
        
        label = QtGui.QLabel("Choose a manufacturer to see available systems:")
        label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        label.setStyleSheet('font-size: 15em; color: silver;')
        header_font = QtGui.QFont("Times",18,QtGui.QFont.Bold)
        label.setFont(header_font)
        layout.addWidget(label)

        
                
        for mfg, systems in self.systems.items():
            icon_path = self.mfg_icon_basepath + mfg + '\\manufacturer.png'
            self.buttons.append(QtGui.QPushButton('',self))
            self.buttons[-1].setIcon(QtGui.QIcon(icon_path))
            self.buttons[-1].setIconSize(QtCore.QSize(128,128))
            self.buttons[-1].clicked.connect(partial(self.handleButton,data=systems))
            layout.addWidget(self.buttons[-1],1,i)
            
            label = QtGui.QLabel(mfg.capitalize())
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            label.setStyleSheet('color: silver; padding: 5px; text-align: center;')
            layout.addWidget(label,2,i)
            i += 1
        self.setWindowTitle("CeMPulator")
        
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
