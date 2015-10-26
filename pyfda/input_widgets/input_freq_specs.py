# -*- coding: utf-8 -*-
"""
Widget for entering frequency specifications

Author: Christian Münker
"""
# TODO: using objectName is an ugly hack that causes problems in Python 2
from __future__ import print_function, division, unicode_literals, absolute_import
import sys, os
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal

import pyfda.filterbroker as fb    
from pyfda.simpleeval import simple_eval

class InputFreqSpecs(QtGui.QWidget):
    """
    Build and update widget for entering the frequency
    specifications like F_sb, F_pb etc.
    """

    # class variables (shared between instances if more than one exists)
    sigSpecsChanged = pyqtSignal() # emitted when filter has been changed

    def __init__(self, DEBUG = True, title = "Frequency Specs"):

        super(InputFreqSpecs, self).__init__()
        self.DEBUG = DEBUG
        self.title = title

        self.qlabels = []    # list with references to QLabel widgets
        self.qlineedit = [] # list with references to QLineEdit widgets

        self._init_UI()


#-------------------------------------------------------------
    def _init_UI(self):
        """
        Initialize the User Interface
        """
        self.layVMain = QtGui.QVBoxLayout() # Widget main layout

        bfont = QtGui.QFont()
        bfont.setBold(True)
#            bfont.setWeight(75)
        self.lblTitle = QtGui.QLabel(self) # field for widget title
        self.lblTitle.setText(str(self.title))
        self.lblTitle.setFont(bfont)
        self.lblTitle.setWordWrap(True)
        self.layVMain.addWidget(self.lblTitle)
        
        # Create a gridLayout consisting of QLabel and QLineEdit fields
        # for the frequency specs:
        self.layGSpecWdg = QtGui.QGridLayout() # sublayout for spec fields        

        sfFrame = QtGui.QFrame()
        sfFrame.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        sfFrame.setLayout(self.layGSpecWdg)

        self.layVMain.addWidget(sfFrame)
        self.layVMain.setContentsMargins(1,1,1,1)
        self.setLayout(self.layVMain)

        # - Build a list from all entries in the fil_dict dictionary starting
        #   with "F" (= frequency specifications of the current filter)
        # - Pass the list to updateUI which recreates the widget
        newLabels = [str(l) for l in fb.fil[0] if l[0] == 'F']
        
        self.update_UI(newLabels = newLabels)


        # =========== SIGNALS & SLOTS =======================================
        
        # DYNAMIC SIGNAL SLOT CONNECTION:
        # Every time a field is edited, call self._store_entries 
        # This signal-slot connection is constructed in self._add_entry / 
        # destructed in self._del_entry each time the widget is updated, 
        # i.e. when a new filter design method is selected.

        
#-------------------------------------------------------------
    def update_UI(self, newLabels = []):
        """
        Set labels and get corresponding values from filter dictionary.
        When number of elements changes, the layout of subwidget is rebuilt.
        """
        # Check whether the number of entries has changed
        for i in range(max(len(self.qlabels), len(newLabels))):
             # newLabels is shorter than qlabels -> delete the difference
            if (i > (len(newLabels)-1)):
                self._del_entry(len(newLabels))

            # newLabels is longer than existing qlabels -> create new ones!
            elif (i > (len(self.qlabels)-1)):
             self._add_entry(i,newLabels[i])

            else:
                # when entry has changed, update label and corresponding value
                if str(self.qlineedit[i].objectName()) != newLabels[i]:
                    self.qlabels[i].setText(self._rt_label(newLabels[i]))
                    self.qlineedit[i].setText(
                        str(fb.fil[0][newLabels[i]] * fb.fil[0]['f_S']))
                    self.qlineedit[i].setObjectName(newLabels[i])  # update ID

        self._store_entries()         # sort & store values to dict for the case 
                                    # that the response type has been changed 
                                    # eg. from LP -> HP, changing the order 
                                    # of frequency entries


#-------------------------------------------------------------        
    def load_entries(self):
        """
        Reload textfields from filter dictionary 
        Transform the displayed frequency spec input fields according to the units
        setting. Spec entries are always stored normalized w.r.t. f_S in the
        dictionary; when f_S or the unit are changed, only the displayed values
        of the frequency entries are updated, not the dictionary!
        
        Finally, the frequency specs are sorted (when the corresponding button
        is pressed) and stored in the filter dictionary.

        loadEntries is called during init and when a lineedit field has been edited

        It should be called when sigSpecsChanged or sigFilterDesigned is emitted
        at another place, indicating that a reload is required.
        """

        # recalculate displayed freq spec values for (maybe) changed f_S
        for i in range(len(self.qlineedit)):
            f = fb.fil[0][str(self.qlineedit[i].objectName())] * fb.fil[0]['f_S']
            self.qlineedit[i].setText(str(round(f,11)))

        self._store_entries(signal = False)


#-------------------------------------------------------------
    def _rt_label(self, label):
        """
        Rich text label: Format label with italic + bold HTML tags and
         replace '_' by HTML subscript tags
        """
        #"<b><i>{0}</i></b>".format(newLabels[i])) # update label
        if "_" in label:
            label = label.replace('_', '<sub>')
            label += "</sub>"
        htmlLabel = "<b><i>"+label+"</i></b>"
        return htmlLabel


#-------------------------------------------------------------
    def _del_entry(self,i):
        """
        Delete entry number i from subwidget (QLabel and QLineEdit) and
        disconnect the lineedit field from self._sort_store_entries.
        """
        self.qlineedit[i].editingFinished.disconnect(self._store_entries) # needed?

        self.layGSpecWdg.removeWidget(self.qlabels[i])
        self.layGSpecWdg.removeWidget(self.qlineedit[i])

        self.qlabels[i].deleteLater()
        del self.qlabels[i]
        self.qlineedit[i].deleteLater()
        del self.qlineedit[i]


#-------------------------------------------------------------
    def _add_entry(self, i, newLabel):
        """
        Append entry number i to subwidget (QLabel und QLineEdit) and connect
        QLineEdit widget to self._sort_store_entries. This way, the central filter
        dictionary is updated automatically when a QLineEdit field has been
        edited.
        """
        self.qlabels.append(QtGui.QLabel(self))
        self.qlabels[i].setText(self._rt_label(newLabel))

        self.qlineedit.append(QtGui.QLineEdit(
                                    str(fb.fil[0][newLabel]*fb.fil[0]['f_S'])))
        self.qlineedit[i].setObjectName(newLabel) # update ID
        
        self.qlineedit[i].editingFinished.connect(self._store_entries)

        self.layGSpecWdg.addWidget(self.qlabels[i],(i+2),0)
        self.layGSpecWdg.addWidget(self.qlineedit[i],(i+2),1)

#-------------------------------------------------------------
    def _store_entries(self, signal = True):
        """
        - Sort spec entries with ascending frequency if sort button is activated
        - Store specification entries in filter dictionary:
          Entries are normalized with sampling frequency fb.fil[0]['f_S'] !
          The unit scale factor (khz, ...) is contained neither in f_S nor in 
          the specs, hence, it cancels out.
        - Emit sigSpecsChanged signal
        """

        if fb.fil[0]['freq_specs_sort']:
            fSpecs = [simple_eval(self.qlineedit[i].text())
                                            for i in range(len(self.qlineedit))]
            fSpecs.sort()
            
            for i in range(len(self.qlineedit)):
                self.qlineedit[i].setText(str(fSpecs[i]))
           
        for i in range(len(self.qlineedit)):
            fb.fil[0].update(
                {str(self.qlineedit[i].objectName()):round(
                    simple_eval(self.qlineedit[i].text())/fb.fil[0]['f_S'],11)})
        if signal:
            self.sigSpecsChanged.emit()
        

#------------------------------------------------------------------------------

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    form = InputFreqSpecs()

    form.update_UI(newLabels = ['F_SB','F_SB2','F_PB','F_PB2'])
    form.update_UI(newLabels = ['F_PB','F_PB2'])

    form.show()

    app.exec_()
