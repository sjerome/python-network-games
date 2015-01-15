 # -*- coding: utf-8 -*-
from Agent.Agent import Agent

import networkx as nx
import random
from statistics import mean, median, mode, stdev
# Drawing
import pylab
import matplotlib.font_manager
import matplotlib.pyplot as plt

# Assumes pos starts as None to draw at all
pos = None

def draw_graph(G, colors, labels, layout=nx.shell_layout):
    global pos
    if not pos:
        pos = layout(G)
        plt.figure('Simulation')
        plt.show(block=False)


    plt.figure('Simulation')
    plt.clf()
    
    try:
        nx.draw(G, pos, node_color=colors, node_size=1000, alpha=.8)
        nx.draw_networkx_labels(G,pos,labels=labels,font_family=matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')[11])
    except:
        try:
            new_agents = []
            for a in G.nodes_iter():
                if a not in pos:
                    new_agents.append(a)
            for (a, p) in pos.iteritems():
                if not G.has_node(a):
                    del pos[a]
                    pos[new_agents[0]] = p
                    new_agents = new_agents[1:]
            nx.draw(G, pos, node_color=colors, node_size=1000, alpha=.8)
            nx.draw_networkx_labels(G,pos,labels=labels,font_family=matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')[11])
        except:             
            pos = layout(G)
            nx.draw(G, pos, node_color=colors, node_size=1000, alpha=.8)
            nx.draw_networkx_labels(G,pos,labels=labels,font_family=matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')[11])

    plt.draw()


def default_replace_vertex(NW, agent, replacement=None):
    replacement = replacement or random.choice(NW.get_vertices())
    agent.morph_agent(replacement)

def default_weighting(agent):
    return agent.get_fitness()

def default_get_info(agents):
    agent_info = {'count':{}}
    for a in agents:
        agent_info['count'][a.get_name()] = agent_info['count'][a.get_name()] + 1 if a.get_name() in agent_info['count'] else 1
        for (k, v) in a.get_info().items():
            if k not in agent_info:
                agent_info[k] = {}

            if a.get_name() in agent_info[k]: 
                agent_info[k][a.get_name()].append(v)
            else:
                agent_info[k][a.get_name()] = [v]
    return agent_info

class Network:
    # If pass in N creates network of N cooperators
    # If pass in agents creates network with agents
    # If pass in inital networkx graph G, creates NW with that graph
    # If pass in NW, creates network with that NW
    def __init__(self, N=10, agents=None, G=None, NW=None, layout='spectral_layout', get_info=None):
        if NW:
            self.G = NW.G
        elif G:
            self.G = G
        else:
            if agents:
                agents = agents
            else:
                agents = [Agent() for i in xrange(N)]
            self.G = nx.Graph()
            self.G.add_nodes_from(agents)

        self.get_info_func = get_info or default_get_info
        self.layout = layout

    def get_agent(self, agent):
        return agent

    def get_num_vertices(self):
        return self.G.number_of_nodes()

    def get_num_edges(self):
        return self.G.size()

    def get_vertices(self):
        return self.G.nodes()
        
    def get_vertices_iter(self):
        return self.G.nodes_iter()

    def has_edge(self, a1, a2):
        return self.G.has_edge(a1, a2)

    def get_edges(self):
        return self.G.edges()

    def get_edges_iter(self):
        return self.G.edges_iter()

    def get_non_edges_iter(self):
        return nx.non_edges(self.G)

    def get_random_edge(self):
        vertices = self.get_vertices()
        v1 = random.choice(vertices)
        v2 = random.choice(vertices)
        return (v1, v2)

    def get_random_existing_edge(self):
        return random.choice(self.get_edges())

    def get_random_vertex(self):
        return random.choice(self.get_vertices())

    def get_random_vertices(self, n=1):
        return random.sample(self.get_vertices(), n)

    def get_random_vertex_not_equal_to_agent(self, agent=None):
        v1 = self.get_random_vertex()
        if v1 == agent and self.get_num_vertices() == 1:
            return None

        while v1 == agent:
            v1 = self.get_random_vertex()

        return v1

    def get_weighted_random_vertex(self, f=default_weighting):
        total_fitness = sum([f(a) for a in self.get_vertices_iter()])
        
        if total_fitness <= 0.0:
            return self.get_random_vertex()

        tot = 0
        r = random.random()
        for a in self.get_vertices_iter():
            tot += float(f(a))/float(total_fitness)
            if r < tot:
                return a

    def get_deaths(self):
        return [a for a in self.get_vertices_iter() if a.has_died()]

    def neighbors(self, agent):
        return self.G.neighbors(agent)

    def add_edge(self, a1, a2):
        a1 = self.get_agent(a1)
        a2 = self.get_agent(a2)

        self.G.add_edge(a1, a2)

    def remove_edge(self, a1, a2):
        a1 = self.get_agent(a1)
        a2 = self.get_agent(a2)

        self.G.remove_edge(a1, a2)

    def add_vertex(self, agent=None, neighbors=[]):
        a = agent or Agent()
        self.G.add_node(a)
        self.G.add_edges_from([(a, v) for v in neighbors])

    def add_vertices(self, N=1, agents=None, neighbors=None):
        if agents and neighbors:
            for i, a in enumerate(agents):
                self.add_vertex(agents[i], neighbors[i])
        elif agents and not neighbors:
            for a in agents:
                self.add_vertex(agents[i])
        else:
            for i in xrange(N):
                self.add_vertex()

    def remove_vertex(self, agent=None):
        agent = agent or self.get_random_vertex()

        for v in self.get_vertices_iter():
            v.removed_agent(agent)

        self.G.remove_node(agent)

        del agent

    def remove_vertices(self, agents):
        for a in agents:
            self.remove_vertex(a)

    def replace_vertex(self, agent, replace=default_replace_vertex, replacement=None, delete_history=True):
        replace(NW=self, agent=agent, replacement=replacement)
        if delete_history:
            for v in self.get_vertices_iter():
                v.removed_agent(other_agent=agent)

    def replace_vertices(self, agents, replace=default_replace_vertex, replacements=None, delete_history=True):
        if replacements:
            for i, a in enumerate(agents):
                self.replace_vertex(agent=a, replace=replace, replacement=replacements[i], delete_history=delete_history)            
        else:
            for a in agents:
                self.replace_vertex(agent=a, replace=replace, delete_history=delete_history)

    # Updates the network according to a function f
    def update(self, rewire, t=-1):
        rewire(NW=self, t=t)

    # Gets NW information. Total c, total d, cluster coefficient, etc.
    def get_info(self, t=-1):
        self.info = {'agent_information':self.get_info_func(self.get_vertices())}
        self.info['cc'] = "%.2f"%nx.average_clustering(self.G)
        return self.info

    def __str__(self):
        return str([a.get_name() for a in self.get_vertices_iter()]) +'\n' + str([(a1.get_name(), a2.get_name()) for (a1, a2) in self.get_edges_iter()])

    def draw_NW(self, layout=None):
        self.layout = layout or self.layout

        if self.layout == 'shell_layout':
            LO = nx.shell_layout
        elif self.layout == 'spectral_layout':
            LO = nx.spectral_layout
        else:
            LO = nx.circular_layout

        colors = []
        labels = {}

        fitnesses = [a.get_fitness() for a in self.get_vertices_iter()]

        average_fitness = mean(fitnesses)
        std_fitness = stdev(fitnesses) if len(fitnesses) > 1 else .01

        for a in self.get_vertices_iter():
            colors.append(a.get_color(avg=average_fitness, std=std_fitness))
            labels[a] = a.get_label()
        
        draw_graph(G=self.G, colors=colors, labels=labels, layout=LO)

    def print_edges(self):
        print [(a1.get_name(), a2.get_name()) for (a1, a2) in self.get_edges_iter()]
        
    # Prints vertices
    def print_vertices(self):
        print [a.get_name() for a in self.get_vertices_iter()]

    # Prints NW
    def print_nw(self):
        self.print_vertices()
        self.print_edges()

if __name__ == "__main__":
    nw = Network()
    nw.print_nw()