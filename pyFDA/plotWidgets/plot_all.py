# -*- coding: utf-8 -*-
"""

Edited by Christian Münker, 2013
"""
from __future__ import print_function, division, unicode_literals 
import sys, os
# import EITHER PyQt4 OR PySide, depending on your system:
from PyQt4 import QtGui #, QtCore  
#from PySide.QtCore import *
#from PySide.QtGui import *


#import numpy as np
#import scipy.signal as sig
if __name__ == "__main__": # relative import if this file is run as __main__
    cwd=os.path.dirname(os.path.abspath(__file__))
    sys.path.append(cwd + '/..')
import plot_hf, plot_phi


class plotAll(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.pltHf = plot_hf.PlotHf()
        self.pltPhi = plot_phi.PlotPhi()
        
        self.initUI()
        
    def initUI(self):
        """ Initialize UI with tabbed subplots """
        tab_widget = QtGui.QTabWidget()
        tab_widget.addTab(self.pltHf, '|H(f)|')
        tab_widget.addTab(self.pltPhi, 'phi(f)')
        
#        butDraw = QtGui.QPushButton("&No Function")
#        butDraw.clicked.connect(self.redrawAll)
        
#        hbox = QtGui.QHBoxLayout()
#        hbox.addWidget(butDraw)
#        hbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(tab_widget)
#        
        self.setLayout(vbox)

        
    def update(self):
        """ Update and redraw all subplots with new coefficients"""
        self.pltHf.draw()
        self.pltPhi.draw()
#        self.redrawAll()

#    def redrawAll(self):
#        """ Redraw all subplots"""
#        self.pltHf.redraw()
#        self.pltPhi.redraw()             

#------------------------------------------------------------------------
    
def main():
    app = QtGui.QApplication(sys.argv)
    form = plotAll()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()