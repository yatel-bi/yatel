#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice 
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module contains a gui of the main widget.

"""


#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui, QtCore

from yatel.gui import uis
from yatel.gui import double_slider
from yatel.gui import error_dialog
from yatel.gui import sheditor
from yatel.gui import ipython


#===============================================================================
# 
#===============================================================================

class ExplorerFrame(uis.UI("ExplorerFrame.ui")):
    """This is the frame make all explorations
    
    """
    
    #: Signal emited when the save status of the exploration is chaged.
    saveStatusChanged = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent, yatel_connection, saved=True):
         """Create a new instance of ``ExplorerFrame``, also load the latest
         version from a database (if the latest version hasn't topology info
         create a new one with a random topology).
         
        **Params**
            :parent: A gui parent of this widget.
            :action: A conection to the database.
            :saved: If the status of the connection is saved.
            
        """
        
        super(ExplorerFrame, self).__init__(parent=parent)
        
        from yatel.gui import network
        
        self._is_saved = saved
        self._version = ()
        self._startw, self._endw = None, None
        
        self.conn = yatel_connection
        
        self.ipythonWidget = ipython.IPythonWidget()
        self.consoleLayout.addWidget(self.ipythonWidget)
        self.ipythonWidget.reset_ns(explorer=self)
        msg = ("\nUse:\n" 
               "    'explorer' -> all context gui.\n"
               "    'explorer.conn' -> context connection\n"
               "    'explorer.network' ->  the network graph\n")
        self.ipythonWidget.write(self.tr(msg))
        
        self.network = network.NetworkProxy()
        self.network.widget.setParent(self)
        self.network.node_clicked.conectar(self.on_node_clicked)
        self.pilasLayout.addWidget(self.network.widget)
        
        self.hapSQLeditor = sheditor.HiglightedEditor("sql")
        self.hapSQLLayout.addWidget(self.hapSQLeditor)
        self.hapSQLeditor.textChanged.connect(self.on_hapSQLeditor_textChanged)
        
        version = self.conn.get_version() # the latest
                
        minw, maxw = [e.weight or 0 for e in self.conn.min_max_edge()]
        minw = int(minw) - (1 if minw > int(minw) else 0)
        maxw = int(maxw) + (1 if maxw > int(maxw) else 0)
        self.rs = double_slider.DoubleSlider(self,
                                             self.tr("Weights"),
                                             minw, maxw)
        self.rs.endValueChanged.connect(self.on_weightEnd_changed)
        self.rs.startValueChanged.connect(self.on_weightStart_changed)
        self.sliderLayout.addWidget(self.rs)
        
        # load latest version
        self.load_version(version)
        if version["id"] == 1:
            self.save_version("topology_added", "added topological info")
        self.tabWidget.setCurrentIndex(0)
    
    def _set_unsaved(self):
        self._is_saved = False
        self.saveStatusChanged.emit(self._is_saved)
        
    def _add_filter(self, checked, ambient):
        facts_and_values = {}
        for att in ambient.keys():
            facts_and_values[att] = self.conn.get_fact_attribute_values(att)
        if facts_and_values:
            row = self.enviromentsTableWidget.rowCount()
            self.enviromentsTableWidget.insertRow(row)
            envWidget = EnviromentListItem(env=facts_and_values)
            checkbox = QtGui.QCheckBox()
            checkbox.stateChanged.connect(self.on_filter_changed)
            envWidget.filterChanged.connect(self.on_filter_changed)
            envWidget.removeRequested.connect(self.on_filter_removeRequested)
            self.enviromentsTableWidget.setCellWidget(row, 0, checkbox)
            self.enviromentsTableWidget.setCellWidget(row, 1, envWidget)
            checkbox.setChecked(checked)
            for att, value in ambient.items():
                envWidget.select_attribute_value(att, value)
            size = envWidget.size().height() \
                   if row == 0 else \
                   self.enviromentsTableWidget.rowHeight(0)
            self.enviromentsTableWidget.setRowHeight(row, size)
    
    #===========================================================================
    # SLOTS
    #===========================================================================
    
    def on_haplotypesNamesCheckBox_stateChanged(self, state):
        """Slot executed when ``haplotypesNamesCheckBox`` state changed.
        
        If the ``state`` is *True* the names of the haplotypes are showed.
        
        **Params**
            :state: ``bool`` value if the checkbox is checked or not.

        """
        self.network.show_haps_names(bool(state))
        
    def on_weightsCheckBox_stateChanged(self, state):
        """Slot executed when ``weightsCheckBox`` state changed.
        
        If the ``state`` is *True* the weights of the edges are showed. 
        
        **Params**
            :state: ``bool`` value if the checkbox is checked or not.

        """
        self.network.show_weights(bool(state))
    
    @QtCore.pyqtSlot(int)
    def on_tabWidget_currentChanged(self, idx):
        """Slot executed when ``tabWidget`` tab change.
        
        If the ``idx`` is *0* the execute the slot ``on_filter_changed``
        otherwise ``NetworkProxy.unhighlightall``.
        
        Save status is setted  to ``False``.
        
        **Params**
            :idx: Index of the current tab as ``int``.

        """
        if idx == 0:
            self.on_filter_changed()
        else:
            self.network.unhighlightall()
    
    def on_hapSQLeditor_textChanged(self):
        """Slot executed when ``hapSQLeditor`` text changed.
        
        If the editor is empty the ``executeHapSQL`` is disabled.
        
        Save status is setted  to ``False``.

        """
        text = self.hapSQLeditor.text().strip()
        self.executeHapSQLButton.setEnabled(bool(text))
        self._set_unsaved()
    
    @QtCore.pyqtSlot()
    def on_executeHapSQLButton_clicked(self):
        """Slot executed when ``hapSQLButton`` are clicked.
        
        Executes the sql query over all haplotypes of the connection and
        highligth the result in the network.

        """        
        try:
            query = self.hapSQLeditor.text().strip()
            if not query.lower().startswith("select"):
                msg = "The query must be start with the 'select' command"
                raise ValueError(msg)
            haps = self.conn.hap_sql(query)
            if haps:
                self.network.highlight_nodes(*haps)
            else:
                self.network.unhighlightall()
        except Exception as err:
            error_dialog.critical(self.tr("Error on Haplotype SQL"), err)
            
    def on_weightStart_changed(self, start):
        """Slot executed when the doble slider representing the the lower limit 
        of the weights to be showed change.
        
        This execute a query ober the database and filter all edges to show.
        
        Save status is setted  to ``False``.
        
        """
        if start != self._startw:
            edges = tuple(self.conn.filter_edges(start, self._endw))
            self.network.filter_edges(*edges)
            self._startw = start
            self._set_unsaved()
    
    def on_weightEnd_changed(self, end):
        """Slot executed when the doble slider representing the the upper limit 
        of the weights to be showed change.
        
        This execute a query ober the database and filter all edges to show.
        
        Save status is setted  to ``False``.
        
        """
        if end != self._endw:
            edges = tuple(self.conn.filter_edges(self._startw, end))
            self.network.filter_edges(*edges)
            self._endw = end
            self._set_unsaved()
    
    @QtCore.pyqtSlot()
    def on_addEnviromentPushButton_clicked(self):
        """Slot executed when ``addEnviromentPushButton`` are clicked.
        
        This method open a ``EnviromentDialog`` instance for configure the
        new filter and if its accepted add a new filter to the ambien table.
        
        Save status is setted  to ``False``.
        
        """   
        self.envDialog = EnviromentDialog(self,
                                          self.conn.facts_attributes_names())
        if self.envDialog.exec_():
            atts = self.envDialog.selected_attributes
            ambient = dict((att, None) for att in atts)
            self._add_filter(False, ambient)
            self._set_unsaved()
        self.envDialog.setParent(None)
        self.envDialog.destroy()
        del self.envDialog
    
    def on_filter_removeRequested(self, widget):
        """Slot executed when *remove* button of a filter are clicked.
        
        This method remove a parent row of the widget.
        
        Save status is setted  to ``False``.
        
        **Params**
            :widget: The widget to be removed from the ambient table.
        
        """   
        for ridx in range(self.enviromentsTableWidget.rowCount()):
            if self.enviromentsTableWidget.cellWidget(ridx, 1) == widget:
                check = self.enviromentsTableWidget.cellWidget(ridx, 0)
                if check.isChecked():
                    check.setChecked(False)
                    self.on_filter_changed()
                self.enviromentsTableWidget.removeRow(ridx)
                check.stateChanged.disconnect(self.on_filter_changed)
                widget.removeRequested.disconnect(self.on_filter_removeRequested)
                widget.filterChanged.disconnect(self.on_filter_changed)
                self._set_unsaved()
                break
    
    def on_filter_changed(self):
        """Slot executed when a combo box of a filter or a checkbox status 
        change.
        
        This method iterates over all ambients and highlight all match nodes.
        
        Save status is setted  to ``False``.

        """   
        haps = []
        for ridx in range(self.enviromentsTableWidget.rowCount()):
            check = self.enviromentsTableWidget.cellWidget(ridx, 0)
            if check.isChecked():
                envwidget = self.enviromentsTableWidget.cellWidget(ridx, 1)
                for hap in self.conn.ambient(**envwidget.filters()):
                    haps.append(hap)
        if haps:
            self.network.highlight_nodes(*haps)
        else:
            self.network.unhighlightall()
        self._set_unsaved()
    
    @QtCore.pyqtSlot(int)
    def on_hapsComboBox_currentIndexChanged(self, idx):
         """Slot executed when a ``hapsComboBox`` index change. 
        
        The method charge ``attTableWidget`` with the selected haplotype.
        
        **Params**
            :idx: The new index of the ``hapsComboBox``.
        
        """
        hap = self.hapsComboBox.itemData(idx)
        atts = hap.items_attrs()
        atts.sort()
        self.network.select_node(hap)
        self.attTableWidget.clearContents()
        self.attTableWidget.setRowCount(len(atts))
        for idx, atts in enumerate(atts):
            nameitem = QtGui.QTableWidgetItem(atts[0])
            valueitem = QtGui.QTableWidgetItem(unicode(atts[1]))
            self.attTableWidget.setItem(idx, 0, nameitem)
            self.attTableWidget.setItem(idx, 1, valueitem)
    
    def on_node_clicked(self, evt):
        """Slot executed when a *node* is clicked in the network.
        
        NOTE: this is a **Pilas** slot.
        
        This method select the index of the haplotype in ``hapsComboBox`` and
        execute the ``on_hapsComboBox_currentIndexChanged`` slot.
        
        **Params**
            :evt: A ``dict`` with the key ``node`` with value is the haplotype
                  clicked.
        
        """
        hap = evt["node"]
        self._set_unsaved()
        for idx in range(self.hapsComboBox.count()):
            actual_hap = self.hapsComboBox.itemData(idx)
            if hap == actual_hap:
                self.hapsComboBox.setCurrentIndex(idx)

    #===========================================================================
    # PUBLIC
    #===========================================================================
    
    def remove_all_filters(self):
        """Removes all filters from ambient table.
        
        """
        for ridx in range(self.enviromentsTableWidget.rowCount()):
            widget = self.enviromentsTableWidget.cellWidget(ridx, 1)
            check = self.enviromentsTableWidget.cellWidget(ridx, 0)
            if check.isChecked():
                check.setChecked(False)
                self.on_filter_changed()
            self.enviromentsTableWidget.removeRow(ridx)
            check.stateChanged.disconnect(self.on_filter_changed)
            widget.removeRequested.disconnect(self.on_filter_removeRequested)
            widget.filterChanged.disconnect(self.on_filter_changed)
        self._set_unsaved()
    
    def load_version(self, version):
        """Load a version ``dict``.
        
        **Params**
            :version: A ``dict`` to setup all the gui of the explorer.
            
        """
        try:
            self.network.clear()
            
            if None in version["weight_range"]:
                version["weight_range"] = self.rs.tops()
            self._startw, self._endw = version["weight_range"]
            self.rs.setStart(self._startw)
            self.rs.setEnd(self._endw)
            
            if not version["hap_sql"]:
                version["hap_sql"] = "SELECT * FROM `haplotypes`"
            if not version["topology"]:
                for hap in self.conn.iter_haplotypes():
                    version["topology"][hap] = self.network.get_unussed_coord()
            for hap, xy in sorted(version["topology"].items(), key=lambda h: h[0].hap_id):
                self.network.add_node(hap, x=xy[0], y=xy[1])
                self.hapsComboBox.addItem(unicode(hap.hap_id), hap)
            
            self.remove_all_filters()
            for checked, ambient in version["ambients"]:
                self._add_filter(checked, ambient)
            
            for edge in self.conn.iter_edges():
                self.network.add_edge(edge)
                
            self.hapSQLeditor.setText(version["hap_sql"])
            
            self._is_saved = True
            self._version = (version["id"], version["datetime"], version["tag"])       
            self.saveStatusChanged.emit(self._is_saved)
            self.on_tabWidget_currentChanged(self.tabWidget.currentIndex())
        except Exception as err:
            error_dialog.critical(self.tr("Load Error"), err)
    
    def is_saved(self):
        """Return a ``bool`` representing if the exploraton status of the 
        explorer change from the last save.
        
        """
        return self._is_saved
    
    def save_version(self, new_version, comment):
        """Save the current status of the exploration to the database.
        
        Save status is setted  to ``True``.
        
        **Params**
            :new_version: The new name of the version (like *0.1* or *1.5.2b*).
            :comment: A coment about the new version.
        
        """
        try:
            topology = self.network.topology()
            weight_range = self._startw, self._endw
            sql = self.hapSQLeditor.text().strip()
            ambients = []
            for ridx in range(self.enviromentsTableWidget.rowCount()):
                check = self.enviromentsTableWidget.cellWidget(ridx, 0)
                envwidget = self.enviromentsTableWidget.cellWidget(ridx, 1)
                ambients.append((check.isChecked(), envwidget.filters()))
            self.conn.save_version(new_version, comment, sql, topology,
                                   weight_range, ambients)
            self._is_saved = True
            self.saveStatusChanged.emit(self._is_saved)
        except Exception as err:
            error_dialog.critical(self.tr("Save Error"), err)
        
    def destroy(self):
        """Destroy the explorer widget"""
        self.network.clear()
        self.network.setParent(None)
        self.pilasLayout.removeWidget(self.network.widget)
        super(ExplorerFrame, self).destroy()
        
    def version(self):
        """Return the actual version of the exploration
        
        **Return**
            A ``dict`` with info about the version.
            
        """
        return self._version


#===============================================================================
# EVIROMENT DIALOG
#===============================================================================

class EnviromentDialog(uis.UI("EnviromentDialog.ui")):
    
    def __init__(self, parent, facts_names):
        super(EnviromentDialog, self).__init__(parent=parent)
        self.factAttributesListWidget.addItems(facts_names)
        self.factAttributesListWidget.sortItems()
    
    def on_factAttributesListWidget_currentItemChanged(self, entered, exited):
        self.addButton.setEnabled(bool(entered))
        
    def on_selectedAttributesListWidget_currentItemChanged(self, entered, exited):
        self.removeButton.setEnabled(bool(entered))
    
    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        idx = self.factAttributesListWidget.currentIndex().row()
        item = self.factAttributesListWidget.takeItem(idx)
        if item:
            self.selectedAttributesListWidget.addItem(item)
            self.selectedAttributesListWidget.sortItems()
            self.factAttributesListWidget.sortItems()
    
    @QtCore.pyqtSlot()
    def on_removeButton_clicked(self):
        idx = self.selectedAttributesListWidget.currentIndex().row()
        item = self.selectedAttributesListWidget.takeItem(idx)
        if item:
            self.factAttributesListWidget.addItem(item)
            self.selectedAttributesListWidget.sortItems()
            self.factAttributesListWidget.sortItems()
        
    @property
    def selected_attributes(self):
        atts = []
        for idx in range(self.selectedAttributesListWidget.count()):
            text = self.selectedAttributesListWidget.item(idx).text()
            atts.append(text)
        return tuple(atts)


#===============================================================================
# ENVIROMENT LIST ITEM
#===============================================================================

class EnviromentListItem(uis.UI("EnviromentListItem.ui")):
    
    filterChanged = QtCore.pyqtSignal()
    removeRequested = QtCore.pyqtSignal('QWidget')
    
    def __init__(self, env):
        super(EnviromentListItem, self).__init__()
        self._filters = {}
        for k, values in sorted(env.items()):
            label = QtGui.QLabel(k)
            self.envLayout.addWidget(label)
            combo = QtGui.QComboBox()
            combo.addItem("", None)
            for v in values:
                combo.addItem(unicode(v), v)
            self.envLayout.addWidget(combo)
            combo.currentIndexChanged.connect(self.on_combo_currentIndexChanged)
            self._filters[k] = combo
        self.setVisible(True)
        
    def on_combo_currentIndexChanged(self, idx):
        self.filterChanged.emit()
    
    def select_attribute_value(self, name, value):
        combo = self._filters[name]
        for idx in range(combo.count()):
            avalue = combo.itemData(idx)
            if value == avalue:
                combo.setCurrentIndex(idx)
                break  
            
    @QtCore.pyqtSlot()
    def on_removeButton_clicked(self):
        self.removeRequested.emit(self)
    
    def filters(self):
        f = {}
        for label_text, combo in self._filters.items():
            idx = combo.currentIndex()
            value = combo.itemData(idx)
            f[label_text] = value
        return f


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

