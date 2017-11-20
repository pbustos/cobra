# /usr/bin/env pytho
# -*- coding: utf-8 -*

from __future__ import print_function
import sys, signal, argparse
from PyQt4 import QtCore, QtGui
from widgets.QNetworkxGraph.QNetworkxGraph import QNetworkxWidget, NodeShapes
from viewer import Viewer
from model import Model
import networkx as nx


class Main():
    """This is the Main class which spawns the objects for the Model,
    Viewer and the Controller, for our MVC model."""

    def __init__(self):
        # parser = argparse.ArgumentParser()
        # parser.add_argument("filename", help="the xml file containing the component graph data")
        # args = parser.parse_args()

        #create model as a NetworkX graph using dict
        self.model = Model()

        # create Qt Ui in a separate class
        self.viewer = Viewer()

        #transfer model to viewer

        for node in self.model.graph.nodes():
             self.viewer.add_node(node)
        print("added nodes:",self.model.graph.number_of_nodes())
        
        for edge in self.model.graph.edges():
            self.viewer.add_edge(edge[0], edge[1], str(self.model.graph.edges[edge[0],edge[1]]['label']))
        print("added edges:", self.model.graph.number_of_edges())

        self.viewer.show()

        initial_pos = nx.random_layout(self.model.graph)
        initial_pos = self.viewer.graph_visualization.networkx_positions_to_pixels(initial_pos)
        self.viewer.graph_visualization.set_node_positions(initial_pos)
        print("added graph nodes:", self.viewer.graph_visualization.nx_graph.number_of_nodes())

	self.viewer.connect(self.viewer.animateButton, QtCore.SIGNAL("clicked()"), self.viewer.animate_button)
        self.viewer.graph_visualization.animate_nodes(True)      


if __name__ == '__main__':
    # process params with a argparse
    app = QtGui.QApplication(sys.argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main = Main()
    ret = app.exec_()
    sys.exit(ret)
