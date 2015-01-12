 # -*- coding: utf-8 -*-
from Network.Network import Network
from Agent.Agent import Agent

import random

def default_rewire(NW, t=-1):
	NW.replace_vertices(NW.get_deaths())	
	(a1, a2) = NW.get_random_edge()

	if NW.has_edge(a1=a1, a2=a2): 
		if a1.should_remove(other_agent=a2) or a2.should_remove(other_agent=a1):
			NW.remove_edge(a1=a1, a2=a2)
	else:
		if a1.should_add(other_agent=a2) and a2.should_add(other_agent=a1):
			NW.add_edge(a1=a1, a2=a2)

class Simulation:
	def __init__(self, N=20, agents=None, G=None, rewire=default_rewire, get_info=None, layout='shell_layout', reset=None):
		if agents:
			self.NW = Network(agents=agents, layout=layout, get_info=get_info)
		elif G:
			self.NW = Network(G=G, layout=layout, get_info=get_info)
		else:
			self.NW = Network(N=N, layout=layout, get_info=get_info)

		self.RW = rewire
		self.reset = reset

	def play(self, t=-1):
		if self.reset and t % self.reset == 0:
			for a in self.NW.get_vertices_iter():
				a.reset_utility()

		for (a1, a2) in self.NW.get_edges_iter():
			s1 = a1.get_behavior(other_agent=a2)
			s2 = a2.get_behavior(other_agent=a1)

			a1.update(other_agent=a2, s={a1:s1, a2:s2}, t=t)
			a2.update(other_agent=a1, s={a1:s1, a2:s2}, t=t)

		for a in self.NW.get_vertices_iter():
			a.tire(t=t)

	def rewire(self, t=-1):
		self.NW.update(rewire=self.RW, t=t)
	
	def draw(self, t=-1, layout=None):
		self.NW.draw_NW(layout=layout)

	def get_info(self, t=-1):
		return self.NW.get_info(t=t)

if __name__ == "__main__":
	sim = Simulation()
	for t in xrange(50):
		sim.play(t=t)
		sim.rewire(t=t)
		sim.draw(t=t)