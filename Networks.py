 # -*- coding: utf-8 -*-

from Network import Network
from Agents import *
import networkx as nx

import random 

def default_get_random_agent(i=0, N=20, types=None):
    return random_agent(types=types)

def default_get_cooperator(i=0, N=20):
    return cooperator()

def default_get_circular_agent(i=0, N=20):
    return defector() if i < int(N/2) else cooperator()

def get_cooperator_or_defector(i=0, N=20):
    return cooperator() if random.random() < .5 else defector()

def circular_graph(N=10, get_agent=default_get_circular_agent):
    agents = [get_agent(i, N) for i in xrange(N)]

    G = nx.Graph()
    for i in xrange(N):
        G.add_edge(agents[i], agents[(i+1)%N])

    return G

def random_graph(N=10, num_edges=10, get_agent=default_get_random_agent, types=None):
    agents = [get_agent(i=i, N=N, types=types) for i in xrange(N)]

    G = nx.Graph()
    G.add_nodes_from(agents)
    edges = set([])

    for i in xrange(num_edges):
        v1 = random.choice(agents)
        while True:
            v2 = random.choice(agents)
            if v1 != v2:
                break
        edges.add((v1, v2))
    G.add_edges_from(list(edges))

    return G

def random_graph_with_agent_types(N=10, num_edges=10, types=None):
    return random_graph(N=N, num_edges=num_edges, get_agent=default_get_random_agent, types=types)

def random_graph_with_CD(N=10, num_edges=10):
    return random_graph_with_agent_types(N=N, num_edges=num_edges, types=[cooperator, defector])

def complete_graph(N=10, get_agent=default_get_cooperator):
    agents = [get_agent(i, N) for i in xrange(N)]
    G = nx.Graph()
    for i in xrange(N):
        for j in xrange(i, N):
            G.add_edge(agents[i], agents[j])
    return G

def complete_graph_with_agent(N=10, get_agent=cooperator):
    def get_agent_at_index(i, N):
        return get_agent()

    return complete_graph(N=N, get_agent=get_agent_at_index)

def complete_graph_cooperators(N=10):
    return complete_graph_with_agent(N=N, get_agent=cooperator)

def complete_graph_defectors(N=10):
    return complete_graph_with_agent(N=N, get_agent=defector)

def complete_graph_random_agents(N=10):
    return complete_graph_with_agent(N=N, get_agent=random_agent)
