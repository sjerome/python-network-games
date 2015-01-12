 # -*- coding: utf-8 -*-

# Simulations:
from Network.Networks import *
from Agent.Agents import *
from Simulation import Simulation
import random

def INV_FIT(N=20, initial=cooperator, mutation_rate=.02, invader=random_agent):
	def FIT_updating(NW, t=-1):
		a = NW.get_weighted_random_vertex()
		child = invader() if random.random() < mutation_rate else a.get_child()
		v1 = NW.get_random_vertex()

		NW.replace_vertex(agent=v1, replacement=child)

	return Simulation(G=complete_graph_with_agent(N=N, agent_type=initial), rewire=FIT_updating, layout='shell_layout')

def INV_UTIL(N=20, mutation_rate=.05, initial=defector, invader=TFT):
	def RW_updating(NW, t=-1):
		deaths = NW.get_deaths()
		replacements = [invader() if random.random() < mutation_rate else defector() for i in xrange(len(deaths))]
		NW.replace_vertices(agents=deaths, replacements=replacements)

	return Simulation(G=complete_graph_with_agent(N=N, agent_type=initial), rewire=RW_updating, layout='shell_layout')

def DYN(N=20, replacement=random_agent, types=None):
	def DYN_updating(NW, t=-1):
		deaths = NW.get_deaths()
		for a in deaths:
			NW.replace_vertex(agent=a, replacement=replacement())

		(v1, v2) = NW.get_random_edge()
		if NW.has_edge(v1, v2): 
			if v1.should_remove(other_agent=v2) or v2.should_remove(other_agent=v1):
				NW.remove_edge(a1=v1, a2=v2)
		else:
			if v1.should_add(other_agent=v2) and v2.should_add(other_agent=v1):
				NW.add_edge(a1=v1, a2=v2)
	
	return Simulation(G=random_graph_with_agent_types(N=N, types= types or [cooperator, defector]), rewire=DYN_updating, layout='shell_layout')

def NC(N=20, reset=None):
	def NC_updating(NW, t=-1):
		NW.replace_vertices(agents=NW.get_deaths())

		if random.random() < .1:
			if random.random() < .5:
				NW.add_vertex(agent=random_agent([cooperator, defector]))
			else:
				if NW.get_num_vertices() >=2:
					NW.remove_vertex(agent=NW.get_random_vertex())

		if random.random() < .1:
			(v1, v2) = NW.get_random_edge()
			if NW.has_edge(a1=v1, a2=v2): 
				NW.remove_edge(a1=v1, a2=v2)
			else:
				NW.add_edge(a1=v1, a2=v2)	

	return Simulation(G=random_graph_with_agent_types(N=N, types=[cooperator, defector]), rewire=NC_updating, layout='shell_layout', reset=reset)

def WM(N=20):
	def WM_updating(NW, t=-1):
		NW.replace_vertices(agents=NW.get_deaths())

	return Simulation(G=complete_graph_with_agent_types(N=N, types=[cooperator, defector]), rewire=WM_updating, layout='shell_layout')

def DB(N=20, reset=1):
	def DB_updating(NW, t=-1):
		v = NW.get_random_vertex()

		neighbors = NW.neighbors(agent=v)

		if neighbors[0].get_fitness() + neighbors[1].get_fitness() == 0.0: 
			replacement = neighbors[random.randrange(0,2)]
		elif random.random() < float(neighbors[0].get_fitness())/float((neighbors[0].get_fitness() + neighbors[1].get_fitness())):
			replacement = neighbors[0]
		else:
			replacement = neighbors[1]

		NW.replace_vertex(agent=v, replacement=replacement.get_child())

	return Simulation(G=circular_graph(N=N), rewire=DB_updating, layout='spectral_layout', reset=reset)

def BD(N=20, reset=1):
	def BD_updating(NW, t=-1):
		v = NW.get_weighted_random_vertex()
		neighbors = NW.neighbors(agent=v)
		NW.replace_vertex(agent=neighbors[random.randrange(0,2)], replacement=v.get_child())

	return Simulation(G=circular_graph(N=N), rewire=BD_updating, layout='spectral_layout', reset=reset)

def FM(N=20, num_edges=0, u=.2, epsilon=.01, mutation_rate=.05, reset=1):
	def FM_updating(NW, t=-1):
		v1 = NW.get_random_vertex()
		p = v1.get_info()['p']
		if random.random() < float(1)/float(1+p):
			if  random.random() < mutation_rate:
				replacement = random_agent(types=[FM_agent_defector, FM_agent_cooperator])
			else:
				picked = NW.get_weighted_random_vertex()

				if random.random() < u:
					behavior = random.choice([cooperate, defect])
				else:
					behavior = picked.get_behavior_function()

				p_role_model = picked.get_info()['p']

				if p_role_model > p:
					new_p = p+epsilon
				elif p_role_model < p:
					new_p = p - epsilon
				else:
					new_p = p
					
				replacement = picked.get_child(behavior=behavior, new_info={'p':p-epsilon})

			NW.replace_vertex(agent=v1, replacement=replacement)
		else:
			v2 = NW.get_random_vertex_not_equal_to_agent(agent=v1)

			if NW.has_edge(a1=v1,a2=v2):
				if v1.should_remove(other_agent=v2):
					NW.remove_edge(a1=v1, a2=v2)
			else:
				if v1.should_add(other_agent=v2) and v2.should_add(other_agent=v1):
					NW.add_edge(a1=v1, a2=v2)

	return Simulation(G=random_graph_with_agent_types(N=N, num_edges=num_edges, types=[FM_agent_defector]), rewire=FM_updating, layout='shell_layout', reset=reset)



