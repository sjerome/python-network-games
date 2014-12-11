 # -*- coding: utf-8 -*-

# Simulations:
from Networks import *
from Agents import *
from Simulation import Simulation
import random

def INV_FIT(N=20, initial=cooperator, mutation_rate=.02, invader=random_agent):
	def FIT_updating(NW, t=-1):
		a = NW.get_weighted_random_vertex()
		child = invader() if random.random() < mutation_rate else a.get_child()
		v1 = NW.get_random_vertex()

		NW.replace_vertex(a=v1, replacement=child)

	return Simulation(G=complete_graph_with_agent(N=N, get_agent=initial), rewire=FIT_updating, layout='shell_layout')

def INV_UTIL(N=20, mutation_rate=.05, initial=defector, invader=TFT):
	def RW_updating(NW, t=-1):
		deaths = NW.get_deaths()
		replacements = [invader() if random.random() < mutation_rate else defector() for i in xrange(len(deaths))]
		NW.replace_vertices(agents=deaths, replacements=replacements)

	initial_graph = complete_graph_with_agent(N=N, get_agent=initial)
	return Simulation(G=initial_graph, rewire=RW_updating, layout='shell_layout')

def DYN(N=20, replacement=random_agent):
	def DYN_updating(NW, t=-1):
		deaths = NW.get_deaths()
		for a in deaths:
			NW.replace_vertex(a=a, replacement=replacement())

		(v1, v2) = NW.get_random_edge()
		if NW.has_edge(v1, v2): 
			if v1.should_remove(v2) or v2.should_remove(v1):
				NW.remove_edge(v1, v2)
		else:
			if v1.should_add(v2) and v2.should_add(v1):
				NW.add_edge(v1, v2)
	
	return Simulation(G=random_graph(N=N), rewire=DYN_updating, layout='shell_layout')

def NC(N=20):
	def NC_updating(NW, t=-1):
		NW.replace_vertices(agents=NW.get_deaths())

		if random.random() < .1:
			if random.random() < .5:
				NW.add_vertex(agent=random_agent())
			else:
				if NW.get_num_vertices() >=2:
					NW.remove_vertex()

		if random.random() < .1:
			(v1, v2) = NW.get_random_edge()
			if NW.has_edge(v1, v2): 
				NW.remove_edge(v1, v2)
			else:
				NW.add_edge(v1, v2)	

	return Simulation(G=random_graph(N=N), rewire=NC_updating, layout='shell_layout')

def WM(N=20):
	def WM_updating(NW, t=-1):
		NW.replace_vertices(agents=NW.get_deaths())

	return Simulation(G=complete_graph_random_agents(N=N), rewire=WM_updating, layout='shell_layout')

def DB(N=20):
	def DB_updating(NW, t=-1):
		v = NW.get_random_vertex()

		neighbors = NW.neighbors(v)

		if neighbors[0].get_fitness() + neighbors[1].get_fitness() == 0.0: 
			replacement = neighbors[random.randrange(0,2)]
		elif random.random() < float(neighbors[0].get_fitness())/float((neighbors[0].get_fitness() + neighbors[1].get_fitness())):
			replacement = neighbors[0]
		else:
			replacement = neighbors[1]

		NW.replace_vertex(a=v, replacement=replacement.get_child())

	return Simulation(G=circular_graph(N=N), rewire=DB_updating, layout='spectral_layout', reset=1)

def BD(N=20):
	def BD_updating(NW, t=-1):
		v = NW.get_weighted_random_vertex()
		neighbors = NW.neighbors(v)
		NW.replace_vertex(a=neighbors[random.randrange(0,2)], replacement=v.get_child())

	return Simulation(G=circular_graph(N), rewire=BD_updating, layout='spectral_layout', reset=1)

def DNWDP(N=20, num_edges=0, delta=.005, u=.2, epsilon=.01):
	def DNWDP_updating(NW, t=-1):
		def delta_selection(agent):
			return agent.get_fitness() + delta

		v1 = NW.get_random_vertex()
		p = v1.get_info()['p']
		if random.random() < float(1)/float(1+p):
			if random.random() < u:
				replacement = NW.get_weighted_random_vertex(f=delta_selection)
			else:
				picked = NW.get_random_vertex()
				p_role_model = picked.get_info()['p']
				if p_role_model > p:
					replacement = picked.get_child(info={'p':p_role_model+epsilon})
				else:
					replacement = picked.get_child(info={'p':p_role_model - epsilon})
			NW.replace_vertex(a=v1, replacement=replacement)
		else:
			v2 = NW.get_random_vertex_not_equal(agent=v1)

			if NW.has_edge(v1,v2):
				if v1.should_remove(v2):
					NW.remove_edge(v1, v2)
			else:
				if v1.should_add(v2):
					NW.add_edge(v1, v2)

	def get_agent(i, N, types=None):
		return FM_agent_cooperator(random.random()) if random.random() < .5 else FM_agent_defector()

	return Simulation(G=random_graph(N=N, num_edges=num_edges, get_agent=get_agent), rewire=DNWDP_updating, layout='shell_layout', reset=1)