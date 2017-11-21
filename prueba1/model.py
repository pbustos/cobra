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


class Model():
    """This is the Model object for our MVC model. It stores the component
    graph and contains the functions needed to manipulate it."""

    def __init__(self):

        # this is the networkx digraph object
        self.graph = nx.DiGraph()

        # this dictionary stores the general configuration informtation about the viewer
        self.generalInformation = dict()

        self._logger = RCManagerLogger().get_logger("RCManager.Model")

        # create model
        self.createModel()

    def createModel(self):
        # Read. "ecoli" and "salmonella" are also valid arguments
        self.model = cobra.test.create_test_model("textbook")

        # print model in a table
        # mets = []
        # for met in model.metabolites:
        #     mets.append([met.id, met.formula, met.name, met.charge, met.compartment])
        # print()
        # print("-----------Metabolites-------------")
        # print(tabulate(mets, headers=['ID', 'Formula', 'Name', 'Charge', 'Comp']))
        #
        # print()
        # reacts = []
        # for react in model.reactions:
        #     reacts.append([react.id, react.name, react.subsystem, react.lower_bound, react.upper_bound])
        # print("-----------Reactions---------------")
        # print(tabulate(reacts, headers=['ID', 'Name', 'Subsystem', 'lower_bound', 'upper_bound']))

        # load model as a graph to NX
        # We use the compound  model in which nodes are reactions and edges are metabolites
        #print('------- Names for nodes -------------')
        #for r in model.reactions:
            ##[r.id, r.name, r.subsystem, r.lower_bound, r.upper_bound]
            #self.add_node({'@alias':r.id})
            ##print(r.id)

        cont = 0
        for r in self.model.reactions:
            if cont > 5:
                break
            cont += 1
            for k,v in r.metabolites.iteritems():
                if v == 1:
                    # The edge comes out. Now find the other end
                    # It has to be in another reaction with the same metabolite and a -1
                    for rr in self.model.reactions:
                        for kk,vv in rr.metabolites.iteritems():
                            if rr != r and kk == k and vv == -1:
                                self.add_edge(r.id,rr.id, k)
                                break
                                #print 'Added edge', r.id, rr.id
#MAL
    def add_node(self, nodedata):
        self.graph.add_node(nodedata['@alias'])
        for key, value in nodedata.items():
            self.graph.node[nodedata['@alias']][key] = value

    def add_edge(self, fromNode, toNode, name):
        self.graph.add_edge(fromNode, toNode, label=name)


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