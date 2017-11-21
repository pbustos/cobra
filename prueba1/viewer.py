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
from widgets.QNetworkxGraph.QNetworkxGraph import QNetworkxWidget, NodeShapes, Circle, Square
from logger import RCManagerLogger
from rcmanagerSignals import CustomSignalCollection
import networkx as nx

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
		self.model = model

		# setup rcmanager UI
		self.setupUi(self)

		# set  window icon
		# self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("share/rcmanager/drawing_green.png")))
		# self.showMaximized()

		# logger object for viewer
		self._logger = RCManagerLogger().get_logger("RCManager.Viewer")

		# set the text window to display the log data
		RCManagerLogger().set_text_edit_handler(self.textBrowser)

		# initialise graph object
		self.add_graph_visualization()

		self.drawTree()

		# connect the various UI components (buttons etc.) to the relevant functions (slots)
		self.setup_actions()

		CustomSignalCollection.viewerIsReady.emit()

	# Ñapismo
	def drawTree(self):
		self.treeWidgetMetabs.setColumnCount(1)
		self.treeWidgetMetabs.setHeaderLabel("Metabolites")
		for m in self.model.metabolites:
			top = QTreeWidgetItem(self.treeWidgetMetabs, [m.name])
			top.addChild(QTreeWidgetItem([m.formula + " -- " + m.id]))
			self.treeWidgetMetabs.insertTopLevelItem(0, top)

		self.treeWidgetReacts.setColumnCount(1)
		self.treeWidgetReacts.setHeaderLabel("Reactions")
		for m in self.model.reactions:
			top = QTreeWidgetItem(self.treeWidgetReacts, [m.name])
			top.addChild(QTreeWidgetItem([m.id + " -- " + m.subsystem]))
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


	def set_background_color(self, color=None):
		if not color:
			color = QtGui.QColorDialog.getColor()
			self.graph_visualization.background_color = color
			self.graph_visualization.setBackgroundBrush(color)


	def add_node(self, node, nodedata=None, position=None, region=None):
		self.graph_visualization.add_node(node, position, region)
		createdNode = self.graph_visualization.get_node(node)['item']

		# if 'componentType' in nodedata.keys():
		#     if str(nodedata['componentType']['@value']) == 'agent':
		#         createdNode.set_node_shape(NodeShapes.SQUARE)
		#         return
		createdNode.node_shape = 2


	def add_edge(self, orig_node, dest_node, edge_label):
		self.graph_visualization.add_edge(first_node=orig_node, second_node=dest_node, label=edge_label)


	def add_graph_visualization(self):
		self.graph_visualization = QNetworkxWidget(directed=True)
		self.graph_visualization.setParent(self.tabWidget.widget(0))


	def get_graph_nodes_positions(self):
		return self.graph_visualization.get_current_nodes_positions()


	def animate_button(checked):
		graph_visualization.animate_nodes(checked)
