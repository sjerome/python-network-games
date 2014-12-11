 # -*- coding: utf-8 -*-
import random
from Network import Network
from Agent import Agent
import Event as zp

def default_rewire(NW, t=-1):
	NW.replace_vertices(zp.deaths)
	zp.set_deaths(set([]))
	
	(v1, v2) = NW.get_random_edge()

	if NW.has_edge(v1, v2): 
		if v1.should_remove(v2) or v2.should_remove(v1):
			NW.remove_edge(v1, v2)
	else:
		if v1.should_add(v2) and v2.should_add(v1):
			NW.add_edge(v1, v2)


class Simulation:
	def __init__(self, N=20, agents=None, G=None, rewire=default_rewire, layout='shell_layout', reset=-1):
		if agents:
			self.NW = Network(agents=agents, layout=layout)
		elif G:
			self.NW = Network(G=G, layout=layout)
		else:
			self.NW = Network(N=N, layout=layout)

		self.RW = rewire
		self.reset = reset

	def play(self, t=-1):
		if self.reset > 0 and t % self.reset == 0:
			for a in self.NW.get_vertices_iter():
				a.reset_utility()

		for (a1, a2) in self.NW.get_edges_iter():
			s1 = a1.get_behavior(a2)
			s2 = a2.get_behavior(a1)

			a1.update(s1, s2, a2, t)
			a2.update(s2, s1, a1, t)

		for a in self.NW.get_vertices_iter():
			a.tire(t)

	def rewire(self, t=-1):
		self.NW.update(self.RW, t)
	
	def draw(self, t=-1, layout=None):
		self.NW.draw_NW(layout=layout)

	def get_info(self):
		return self.NW.get_info()

if __name__ == "__main__":
	sim = Simulation()
	for t in xrange(50):
		sim.play(t=t)
		sim.rewire(t=t)
		sim.draw(t=t)