#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2009-2015 by RoboLab - University of Extremadura
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#

#
# CODE BEGINS
#

import math, random
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QGraphicsScene, QPushButton, QBrush, QColor, QTreeWidget, QTreeWidgetItem
from widgets.QNetworkxGraph.QNetworkxGraph import QNetworkxWidget,  Circle, Square
from widgets.QNetworkxGraph.NodeShapes import NodeShapes
from logger import RCManagerLogger
from rcmanagerSignals import CustomSignalCollection
from chemspipy import ChemSpider
import cv2
import urllib
import numpy as np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

MainWindow = uic.loadUiType("cobraUI2.ui")[0]  # Load the UI

class Viewer(QtGui.QMainWindow, MainWindow):
    """ asdfa """

    def __init__(self, model):
        super(Viewer, self).__init__()

        # Ñapa
        self.model = model.model
        self.graph = model.graph

        # setup rcmanager UI
        self.setupUi(self)
        self.read_settings()

        # logger object for viewer
        self._logger = RCManagerLogger().get_logger("RCManager.Viewer")
        # set the text window to display the log data
        RCManagerLogger().set_text_edit_handler(self.textBrowser)

        # initialise graph object
        self.add_graph_visualization()
        #self.add_tree_visualization()

        for node in self.graph.nodes():
            type = self.graph.nodes[node]['type']
            if type == 'reaction':
                self.add_node(node, tipo=self.graph.nodes[node]['type'], flow=self.graph.nodes[node]['flow'])
            else:
                self.add_node(node, tipo =self.graph.nodes[node]['type'])

        print("added nodes:", self.graph.number_of_nodes())

        for edge in self.graph.edges():
            #label = str(self.model.graph.edges[edge[0], edge[1]]['label'])
            region = str(self.graph.edges[edge[0], edge[1]]['comp'])
            self.add_edge(edge[0], edge[1], label=None)
        print("added edges:", self.graph.number_of_edges())

        self.drawTree()

        # connect the various UI components (buttons etc.) to the relevant functions (slots)
        self.setup_actions()

        CustomSignalCollection.viewerIsReady.emit()

        self.cs = ChemSpider('47598d1f-b9e3-4ac6-9d54-81221fe04536')


    # Ñapismo
    def drawTree(self):
        self.treeWidgetMetabs.setColumnCount(1)
        self.treeWidgetMetabs.setHeaderLabel("Metabolites")
        for m in self.model.metabolites:
            top = QTreeWidgetItem(self.treeWidgetMetabs, [m.id])
            top.addChild(QTreeWidgetItem(['Formula: ' + m.formula]))
            top.addChild(QTreeWidgetItem(['Name: ' + m.name]))
            top.addChild(QTreeWidgetItem(['Charge: ' + str(m.charge)]))
            top.addChild(QTreeWidgetItem(['PNG']))
            self.treeWidgetMetabs.insertTopLevelItem(0, top)
        self.treeWidgetMetabs.sortItems(0, QtCore.Qt.AscendingOrder)

        self.treeWidgetReacts.setColumnCount(1)
        self.treeWidgetReacts.setHeaderLabel("Reactions")
        for r in self.model.reactions:
            top = QTreeWidgetItem(self.treeWidgetReacts, [r.id])
            reaction = QTreeWidgetItem([r.reaction])
            top.addChild(reaction)
            reactionName = QTreeWidgetItem([r.name])
            top.addChild(reactionName)
            products = QTreeWidgetItem(['Products'])
            top.addChild(products)
            for m in r.products:
                products.addChild(
                    QTreeWidgetItem([m.id + '  ' + str(r.get_coefficient(m.id)) + '  ' + m.compartment]))
            reactants = QTreeWidgetItem(['Reactants'])
            top.addChild(reactants)
            for m in r.reactants:
                reactants.addChild(QTreeWidgetItem([m.id + '  ' + str(r.get_coefficient(m.id)) + '  ' + m.compartment]))
            self.treeWidgetReacts.sortItems(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetReacts.insertTopLevelItem(0, top)

    def setup_actions(self):
        CustomSignalCollection.addNode.connect(self.add_node)
        # self.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.tab_index_changed)

        # File menu buttons
        # self.connect(self.actionSave, QtCore.SIGNAL("triggered(bool)"), lambda: self.save_model(False))
        # self.connect(self.actionSave_As, QtCore.SIGNAL("triggered(bool)"), lambda: self.save_model(True))
        # self.connect(self.actionOpen, QtCore.SIGNAL("triggered(bool)"), self.open_model)
        # self.connect(self.actionExit, QtCore.SIGNAL("triggered(bool)"), self.close_model)

        # Edit menu buttons

        # View menu buttons
        #     self.connect(self.actionLogger, QtCore.SIGNAL("triggered(bool)"), self.toggle_logger_view)
        #    self.connect(self.actionComponent_List, QtCore.SIGNAL("triggered(bool)"), self.toggle_component_list_view)
        #   self.connect(self.actionFull_Screen, QtCore.SIGNAL("triggered(bool)"), self.toggle_full_screen_view)

        # Tools menu buttons

        self.connect(self.actionSet_Color, QtCore.SIGNAL("triggered(bool)"), self.set_background_color)
        self.connect(self.actionON, QtCore.SIGNAL("triggered(bool)"), self.graph_visualization.start_animation)
        self.connect(self.actionOFF, QtCore.SIGNAL("triggered(bool)"), self.graph_visualization.stop_animation)

        #self.connect(self.treeWidgetMetabs, QtCore.SIGNAL('itemClicked(QTreeWidgetItem, int)'), self.treewidgetclickedSlot)
        self.treeWidgetMetabs.itemClicked.connect(self.treewidgetMetabsClickedSlot)
    #    self.treeWidgetReacts.itemClicked.connect(self.treewidgetReactsClickedSlot)
        self.graph_visualization.node_selection_changed.connect(self.nodeSelectedSlot)


    def nodeSelectedSlot(self, nodes):
        '''
        Slot activated when a node is selected
        '''
        print "activated", nodes
        if nodes[0] in self.model.metabolites:
            item = self.treeWidgetMetabs.findItems(nodes[0], QtCore.Qt.MatchFixedString)[0]
            self.treeWidgetMetabs.scrollToItem(item)
            self.treeWidgetMetabs.setCurrentItem(item)
            self.treeWidgetMetabs.expandItem(item)
        if nodes[0] in self.model.reactions:
            item = self.treeWidgetReacts.findItems(nodes[0], QtCore.Qt.MatchFixedString)[0]
            self.treeWidgetReacts.scrollToItem(item)
            self.treeWidgetReacts.setCurrentItem(item)
            self.treeWidgetReacts.expandItem(item)
            for i in range(item.childCount()):
                item.child(i).setExpanded(True)

    def treewidgetMetabsClickedSlot(self, w, i):
        if w.text(i) in self.model.metabolites:
            createdNode = self.graph_visualization.get_node(w.text(i))['item']
            self.graph_visualization.scene.setFocus(createdNode)

        if w.text(i) == 'PNG':
            f = str(w.parent().child(1).text(0)).partition("Formula: ")[2]
            print "----------------", w.parent().child(1).text(0)
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            elem = self.cs.search(f)[0]
            print elem.common_name
            req = urllib.urlopen(elem.image_url)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)  # 'load it as it is'
            big = cv2.resize(img, (0, 0), fx=4, fy=4)
            self.graph_visualization.stop_animation()
            QtGui.QApplication.restoreOverrideCursor()
            cv2.imshow(elem.common_name, big)
            if cv2.waitKey() & 0xff == 27: quit()

            # width, height, depth = img.shape
            # pm = QtGui.QPixmap()
            # pm.convertFromImage(QtGui.QImage(img.data, width, height, depth*width, QtGui.QImage.Format_RGB888))
            # popup = QtGui.QDialog(self)
            # popup.setWindowTitle(elem.common_name)
            # label = QtGui.QLabel(popup)
            # label.setPixmap(pm)
            # label.setScaledContents(True)
            # popup.resize(width,height)
            # popup.exec_()


    def set_background_color(self, color=None):
        if not color:
            color = QtGui.QColorDialog.getColor()
            self.graph_visualization.background_color = color
            self.graph_visualization.setBackgroundBrush(color)

    def add_node(self, node, nodedata=None, position=None, tipo=None, flow=40):
        self.graph_visualization.add_node(node, position, tipo)
        createdNode = self.graph_visualization.get_node(node)['item']
        if tipo == 'metabolite':
            createdNode.set_node_shape(NodeShapes.SQUARE)
        elif tipo == 'reaction':
            createdNode.set_node_shape(NodeShapes.CIRCLE)
            size = abs(flow) * 3.0
            if size < 15:
                size = 15
            createdNode.set_size(size)

    def add_edge(self, orig_node, dest_node, label=None):
        #print region
        self.graph_visualization.add_edge(first_node=orig_node, second_node=dest_node, label=label, label_visible=False)

    def add_graph_visualization(self):
        self.graph_visualization = QNetworkxWidget(directed=True)
        self.tabLayOut.addWidget(self.graph_visualization)

    def get_graph_nodes_positions(self):
        return self.graph_visualization.get_current_nodes_positions()

    def animate_button(checked):
        graph_visualization.animate_nodes(checked)

    #def resizeEvent(self, event):
    #	self.graph_visualization.resize(event)
    #	self._logger.info("Resize event in Viewer...")

    def write_settings(self):
        settings = QtCore.QSettings("Cobra-UI")
        settings.beginGroup("MainWindow")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.endGroup()
        settings.beginGroup("CentralWidget")
        settings.setValue("size", self.tabWidget.size())
        settings.setValue("pos", self.tabWidget.pos())
        settings.endGroup()

    def read_settings(self):
        settings = QtCore.QSettings("Cobra-UI")
        settings.beginGroup("MainWindow")
        self.resize(settings.value("size", QtCore.QSize(400, 400)).toSize())
        self.move(settings.value("pos", QtCore.QPoint(200, 200)).toPoint())
        settings.endGroup()
        settings.beginGroup("CentralWidget")
        self.tabWidget.resize(settings.value("size", QtCore.QSize(400, 400)).toSize())
        self.tabWidget.move(settings.value("pos", QtCore.QPoint(200, 200)).toPoint())
        settings.endGroup()


