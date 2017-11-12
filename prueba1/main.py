# /usr/bin/env pytho
# -*- coding: utf-8 -*

from __future__ import print_function
import sys, signal, argparse
from PyQt4 import QtCore, QtGui
from widgets.QNetworkxGraph.QNetworkxGraph import QNetworkxWidget, NodeShapes
from viewer import Viewer
from model import Model

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

        for node, data in self.model.graph.nodes_iter(data=True):
             self.viewer.add_node(node, data)
        print("added nodes:",self.model.graph.number_of_nodes())
        for orig, dest, data in self.model.graph.edges_iter(data=True):
             self.viewer.add_edge(orig, dest, data)
        print("added edges:", self.model.graph.number_of_edges())

        self.viewer.show()
        self.viewer.graph_visualization.animate_nodes(True)


if __name__ == '__main__':
    # process params with a argparse
    app = QtGui.QApplication(sys.argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main = Main()
    ret = app.exec_()
    sys.exit(ret)
