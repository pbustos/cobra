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

import time
import networkx as nx
from PyQt4 import QtCore
import cobra
import cobra.test
from tabulate import tabulate
from logger import RCManagerLogger
import pygraphviz as pgv


class Model():
    """This is the Model object for our MVC model. It stores the component
    graph and contains the functions needed to manipulate it."""

    def __init__(self):

        # this is the networkx digraph object
        self.graph = nx.DiGraph()

        # GraphViz graph
        self.gviz = pgv.AGraph(directed=True)
        self.gviz.read('graph.dot')

        # this dictionary stores the general configuration informtation about the viewer
        self.generalInformation = dict()

        self._logger = RCManagerLogger().get_logger("RCManager.Model")

        # create model
        self.createModel()

        # draw GraphViz
        print("Laying out...")
        self.gviz.draw('graph.png', prog='dot')
        #self.gviz.draw('graph.png', prog='twopi')




    def createModel(self):
        # Read. "ecoli" and "salmonella" are also valid arguments
        self.model = cobra.test.create_test_model("textbook")
        print 'Cobra: nodes=', len(self.model.metabolites),'reactions=', len(self.model.reactions)

        solution = self.model.optimize()
        self.model.summary()
        for r in self.model.reactions:
            print(r.id, "   ", solution.fluxes[r.id])

        print "------------------------------"

        #load model as a graph to NX
        # We use the compound  model in which nodes are reactions and edges are metabolites
        for r in self.model.reactions:
            if abs(solution.fluxes[r.id]) >= 0:
                #print(solution.fluxes[r.id])
                self.graph.add_node(r.id, type='reaction', subsystem=r.subsystem, lower_bound=r.lower_bound, upper_bound=r.upper_bound, flow=solution.fluxes[r.id])
                if abs(solution.fluxes[r.id]) == 0:
                    node = self.gviz.get_node(r.id)
                    self.gviz.add_node(node, color='green', fixedsize='true')
                    #self.gviz.add_node(r.id, shape='diamond', color="green", style='filled')
                else:
                    self.gviz.add_node(r.id, shape='diamond', color="green", style='filled', fixedsize='true')
                    pass
                for m in r.metabolites:
                    self.graph.add_node(m.id, type='metabolite')
                    self.gviz.add_node(m.id, color="red", style='filled')
            else:
                #print "discarded ", r.id
                pass

        cont = 0
        for r in self.model.reactions:
            if abs(solution.fluxes[r.id]) >= 0:
                for k in r.products:
                    self.graph.add_edge(r.id, k.id,  name=k.name, comp=k.compartment)
                    self.gviz.add_edge(r.id, k.id)
                for k in r.reactants:
                    self.graph.add_edge(k.id, r.id,  name=k.name, comp=k.compartment)
                    self.gviz.add_edge(k.id, r.id)
        print 'Model: added edges ', self.graph.number_of_edges()


    def add_node(self, nodedata):
        pass

    def add_edge(self, fromNode, toNode, name):
        self.graph.add_edge(fromNode, toNode, label=name)

    def findMetabolicPaths(self):
        """
        computes all linear subpaths in the graph (without bifurcations)
        """
        #for n in self.graph.nodes:


if __name__ == '__main__':
    # sample test case to see the working of the Model class
    model = Model()

    model.add_node({'@alias': 'A'})
    model.add_node({'@alias': 'B'})
    model.add_node({'@alias': 'C'})
    model.add_node({'@alias': 'D'})

    model.add_edge('A', 'B')
    model.add_edge('B', 'C')
    model.add_edge('B', 'D')
    model.add_edge('C', 'D')
    model.add_edge('D', 'B')

    print "Number of nodes:", model.graph.number_of_nodes()
    print "Number of edges:", model.graph.number_of_edges()
    print "Adjacencies: ", model.graph.adj