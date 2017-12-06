#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cobra.test
import pygraphviz as pgv

# GraphViz graph
gviz = pgv.AGraph(directed=True)
gviz.read('graph.dot')

model = cobra.test.create_test_model("salmonella")
print 'Cobra: nodes=', len(model.metabolites), 'reactions=', len(model.reactions)

solution = model.optimize()

for r in model.reactions:
	if abs(solution.fluxes[r.id]) > 0:
		gviz.add_node(r.id, color='green', fixedsize=True, shape='diamond', style='filled')
	else:
		gviz.add_node(r.id, color='lightgray', fixedsize=True, shape='diamond', style='filled')
	for m in r.metabolites:
			gviz.add_node(m.id, color="red", style='filled')

cont = 0
for r in model.reactions:
	for k in r.products:
		gviz.add_edge(r.id, k.id)
	for k in r.reactants:
		gviz.add_edge(k.id, r.id)

#gviz.layout(prog='dot')
gviz.draw('graph.png',prog='dot')
#gviz.write('graph.dot')
