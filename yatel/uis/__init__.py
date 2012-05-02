
from __future__ import absolute_import

import os

from PyQt4 import QtGui, QtCore

import csvcool

from pycante import EDir

import yatel
from yatel import constants
from yatel import resources
from yatel import csv2dom


#===============================================================================
# CONSTANTS
#===============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

UI = EDir(PATH)


#===============================================================================
# 
#===============================================================================

class ChargeFrame(UI("ChargeFrame.ui")):
    """This is the frame to show for select types of given csv file
    
    """
    
    #: This signal is launched when some column is selected as primary id
    idselected = QtCore.pyqtSignal(name="idselected")
    
    def __init__(self, parent, file_content, csv_path):
        super(ChargeFrame, self).__init__(parent)
        self.file_content = file_content
        self.path = csv_path
        with open(csv_path) as f: 
            self.cool = csvcool.read(f, encoding="latin-1")
        self._set_table_cool()
        self._set_table_types()
        self._set_id_of_what()
    
    def _set_id_of_what(self):
        iow = None
        msg = "Please Select '{0}' Column"
        if self.file_content in ("haplotypes", "facts"):
            iow = "Hap ID"
        elif self.file_content in ("weights",):
            iow = "Weight"
        self.tableTypes.horizontalHeaderItem(1).setText(self.tr(iow))
        self.selectHapIdLabel.setText(self.tr(msg.format(iow)))
    
    def _set_table_cool(self):
        """Draw the table containing the csv
        
        """
        self.tableCool.setColumnCount(len(self.cool.columnnames))
        self.tableCool.setRowCount(len(self.cool))
        self.tableCool.setHorizontalHeaderLabels(self.cool.columnnames)
        for cidx, cname in enumerate(self.cool.columnnames):
            for ridx, row in enumerate(self.cool):
                value = row[cname]
                newitem = QtGui.QTableWidgetItem(value)
                self.tableCool.setItem(ridx, cidx, newitem)
        self.tableCool.resizeColumnsToContents()
                
    def _set_table_types(self):
        """Set the data of the table for select the types of all columns
        
        """
        all_types = self.cool.discover_types()
        self.tableTypes.setRowCount(len(all_types))
        self.tableTypes.setVerticalHeaderLabels(self.cool.columnnames)
        types = [(t.__name__, QtCore.QVariant(t)) for t in csvcool.types()]
        for cidx, cname in enumerate(self.cool.columnnames):
            column_type = all_types[cname]
            type_idx = csvcool.types().index(column_type)
            
            radiobutton = QtGui.QRadioButton(self)            
            combo = QtGui.QComboBox(self)
            for t in types:
                combo.addItem(*t)
            combo.setCurrentIndex(type_idx)
            
            self.tableTypes.setCellWidget(cidx, 0, combo)
            self.tableTypes.setCellWidget(cidx, 1, radiobutton)
            
            radiobutton.toggled.connect(self.on_radiobutton_toggled)
        self.tableTypes.resizeColumnsToContents()
    
    # SIGNALS    
    def on_radiobutton_toggled(self, boolean):
        """This funcion is called when some combo is selected for determine
        the id
        
        """
        self.selectHapIdLabel.setVisible(False)
        self.idselected.emit()
    
    @property
    def types(self):
        tps = {}
        for ridx in range(self.tableTypes.rowCount()):
            header = unicode(self.tableTypes.takeVerticalHeaderItem(ridx).text())
            combo = self.tableTypes.cellWidget(ridx, 0)
            tps[header] = combo.itemData(combo.currentIndex()).toPyObject()
        return tps
    
    @property    
    def id_column(self):
        for ridx in range(self.tableTypes.rowCount()):
            radiobutton = self.tableTypes.cellWidget(ridx, 1)
            if radiobutton.isChecked():
                return unicode(
                    self.tableTypes.takeVerticalHeaderItem(ridx).text()
                )


#===============================================================================
# 
#===============================================================================

class ChargeWizard(UI("ChargeWizard.ui")):
    """Wizard for charge csv file as networks
    
    """
    def on_openFileButtonWeights_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
                       self, self.tr("Open Weights File"),
                       constants.HOME_PATH,
                       self.tr("CSV (*.csv)")
                   )
        if filename:
            self.on_closeFileButtonWeights_pressed()
            self.fileLabelWeights.setText(filename)
            self.weightFrame = ChargeFrame(self.weightsPage, "weights", filename)
            self.weightsLayout.addWidget(self.weightFrame)
            self.closeFileButtonWeights.setEnabled(True)
    
    def on_closeFileButtonWeights_pressed(self):
        if hasattr(self, "weightFrame"):
            self.weightsLayout.removeWidget(self.weightFrame)
            self.weightFrame.destroy()
            self.updateGeometry()
        self.fileLabelWeights.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonWeights.setEnabled(False)
    
    def on_openFileButtonFacts_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
                       self, self.tr("Open Facts File"),
                       constants.HOME_PATH,
                       self.tr("CSV (*.csv)")
                   )
        if filename:
            self.on_closeFileButtonFacts_pressed()
            self.fileLabelFacts.setText(filename)
            self.factsFrame = ChargeFrame(self.factsPage, "facts", filename)
            self.factsLayout.addWidget(self.factsFrame)
            self.closeFileButtonFacts.setEnabled(True)
    
    def on_closeFileButtonFacts_pressed(self):
        if hasattr(self, "factsFrame"):
            self.factsLayout.removeWidget(self.factsFrame)
            self.factsFrame.destroy()
            self.updateGeometry()
        self.fileLabelFacts.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonFacts.setEnabled(False)
    
    def on_openFileButtonHaps_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
                       self, self.tr("Open Haplotypes File"),
                       constants.HOME_PATH,
                       self.tr("CSV (*.csv)")
                   )
        if filename:
            self.on_closeFileButtonHaps_pressed()
            self.fileLabelHaps.setText(filename)
            self.haplotypesFrame = ChargeFrame(self.hapsPage, "haplotypes", filename)
            self.hapsLayout.addWidget(self.haplotypesFrame)
            self.closeFileButtonHaps.setEnabled(True)
        
    def on_closeFileButtonHaps_pressed(self):
        if hasattr(self, "haplotypesFrame"):
            self.hapsLayout.removeWidget(self.haplotypesFrame)
            self.haplotypesFrame.destroy()
            self.updateGeometry()
        self.fileLabelHaps.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonHaps.setEnabled(False)
    
            
#===============================================================================
# MAIN WINDOW
#===============================================================================

class MainWindow(UI("MainWindow.ui")):
    """The main window class"""
        
    def setWindowTitle(self, prj=""):
        title = "{0} v.{1} - {2}".format(yatel.__prj__, yatel.__version__, prj)
        super(self.__class__, self).setWindowTitle(title)
    
    def on_actionWizard_triggered(self, *chk):
        if chk:
            self.wizard = ChargeWizard(self)
            self.wizard.exec_()
            
            facts = None
            if hasattr(self.wizard, "factsFrame"):
                facts_data = self.wizard.factsFrame.results
                facts_corrected = facts_data.cool.type_corrector(
                    facts_data.types
                )
                facts = csv2dom.construct_facts(
                    facts_corrected, facts_data.id_column
                )
            
            haplotypes = None
            if hasattr(self.wizard, "haplotypesFrame"):
                haplotypes_data = self.wizard.haplotypesFrame.results
                haplotypes = haplotypes_data.cool.type_corrector(
                    haplotypes_data.types
                )
                haplotypes = csv2dom.construct_haplotypes(
                    haplotypes_corrected, haplotypes_data.id_column
                )
            
            edges = None
            if hasattr(self.wizard, "weightsFrame"):
                weights_data = self.wizard.distancesFrame.results
                weights = weights_data.cool.type_corrector(
                    weights_data.types
                )
                edges = construct_edges(
                    weights_corrected, weights_data.id_column
                )



class SplashScreen(QtGui.QSplashScreen):
    
    def __init__(self):
        pixmap = QtGui.QPixmap(resources.get("splash.png"))
        super(self.__class__, self).__init__(pixmap)




#===============================================================================
# MAIN
#===============================================================================
if __name__ == "__main__":
    print(__doc__)

