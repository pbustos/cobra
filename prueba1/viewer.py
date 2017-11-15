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
from PyQt4.QtGui import QGraphicsScene, QPushButton, QBrush, QColor
from widgets.QNetworkxGraph.QNetworkxGraph import QNetworkxWidget, NodeShapes

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

MainWindow = uic.loadUiType("cobraUI.ui")[0]  # Load the UI

class Viewer(QtGui.QMainWindow, MainWindow):
    """ asdfa """

    def __init__(self):
        super(Viewer, self).__init__()

        # setup rcmanager UI
        self.setupUi(self)

        # set  window icon
        #self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("share/rcmanager/drawing_green.png")))
        #self.showMaximized()

        # initialise graph object
        self.add_graph_visualization()

        #self.set_background_color()

    def set_background_color(self, color=None):
        if not color:
            color = QtGui.QColorDialog.getColor()
            self.graph_visualization.background_color = color
            self.graph_visualization.setBackgroundBrush(color)

    def add_node(self, node, nodedata=None, position=None):
        self.graph_visualization.add_node(node, position)
        createdNode = self.graph_visualization.get_node(node)['item']

        # if 'componentType' in nodedata.keys():
        #     if str(nodedata['componentType']['@value']) == 'agent':
        #         createdNode.set_node_shape(NodeShapes.SQUARE)
        #         return
        createdNode.node_shape=2

    def add_edge(self, orig_node, dest_node, edge_label):
        self.graph_visualization.add_edge(first_node=orig_node, second_node=dest_node, label=edge_label)

    def add_graph_visualization(self):
        self.graph_visualization = QNetworkxWidget()
        self.setCentralWidget(self.graph_visualization)
        
    def get_graph_nodes_positions(self):
        return self.graph_visualization.get_current_nodes_positions()
      
    def animate_button(checked):
      graph_visualization.animate_nodes(checked)
    