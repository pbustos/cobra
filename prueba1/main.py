# /usr/bin/env pytho
# -*- coding: utf-8 -*

from __future__ import print_function
import sys, signal, argparse
from PyQt4 import QtCore, QtGui
from widgets.QNetworkxGraph.QNetworkxGraph import Circle, Square
from viewer import Viewer
from model import Model
import networkx as nx
from logger import RCManagerLogger


class Main():
	"""This is the Main class which spawns the objects for the Model,
    Viewer and the Controller, for our MVC model."""

	def __init__(self):
		# parser = argparse.ArgumentParser()
		# parser.add_argument("filename", help="the xml file containing the component graph data")
		# args = parser.parse_args()

		self._logger = RCManagerLogger().get_logger("RCManager.Model")

		# create model as a NetworkX graph using dict
		self.model = Model()

		# create Qt Ui in a separate class
		self.viewer = Viewer(self.model.model)

		# transfer model to viewer. to be done in Controller

		# create regions
		citoplasma = Circle(QtCore.QPointF(0, 0), 100)
		periplasma = Circle(QtCore.QPointF(0, 0), 80)
		exterior = Circle(QtCore.QPointF(0, 0), 200)

		for node in self.model.graph.nodes():
			self.viewer.add_node(node)
		print("added nodes:", self.model.graph.number_of_nodes())

		for edge in self.model.graph.edges():
			label = str(self.model.graph.edges[edge[0], edge[1]]['label'])
			region = str(self.model.graph.edges[edge[0], edge[1]]['comp'])
			self.viewer.add_edge(edge[0], edge[1], label=label, region=region)
		print("added edges:", self.model.graph.number_of_edges())

		self.viewer.show()

		initial_pos = nx.random_layout(self.model.graph)
		initial_pos = self.viewer.graph_visualization.networkx_positions_to_pixels(initial_pos)
		self.viewer.graph_visualization.set_node_positions(initial_pos)
		self._logger.info("Added " + str(self.viewer.graph_visualization.nx_graph.number_of_nodes()) + " graph nodes")
		self._logger.info("Added " + str(self.viewer.graph_visualization.nx_graph.number_of_edges()) + " graph edges")
		self.viewer.graph_visualization.animate_nodes(False)
		self._logger.info("Simulating now...")

if __name__ == '__main__':
	# process params with a argparse
	app = QtGui.QApplication(sys.argv)
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main = Main()
	ret = app.exec_()
	sys.exit(ret)
