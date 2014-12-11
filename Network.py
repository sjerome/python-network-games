 # -*- coding: utf-8 -*-
from Agent import Agent

import networkx as nx
import random

# Drawing
import pylab
import matplotlib.font_manager
import matplotlib.pyplot as plt
from matplotlib.pyplot import pause

pylab.ion()
pylab.show()

pos = None
def draw_graph(G, colors, labels, layout=nx.shell_layout):
    pylab.clf()

    global pos
    if not pos:
        pos = layout(G)
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

    pylab.draw()


def default_replace_vertex(NW, a, other_agent=None, info=None):
    if other_agent == None:
        other_agent = random.choice(NW.get_vertices())
    a.morph_agent(other_agent)

def default_weighting(a):
    return a.get_fitness()

class Network:
    # If pass in N creates network of N cooperators
    # If pass in agents creates network with agents
    # If pass in inital networkx graph G, creates NW with that graph
    # If pass in NW, creates network with that NW
    def __init__(self, N=10, agents=None, G=None, NW=None, layout='spectral_layout'):
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

        self.info = {}
        self.layout = layout

    def get_agent(self, a):
        return a

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

    def get_random_vertex_not_equal(self, agent):
        v = self.get_random_vertex()
        while v == agent:
            v = self.get_random_vertex()

        return v

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

    def neighbors(self, a):
        return self.G.neighbors(a)

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

    def remove_vertex(self, a=None):
        a = a or self.get_random_vertex()

        for v in self.get_vertices_iter():
            v.removed_agent(a)

        self.G.remove_node(a)

        del a

    def remove_vertices(self, agents):
        for a in agents:
            self.remove_vertex(a)

    def replace_vertex(self, a, replace=default_replace_vertex, replacement=None, info=None, delete_history=True):
        replace(self, a, replacement, info)
        if delete_history:
            for v in self.get_vertices_iter():
                v.removed_agent(a)


    def replace_vertices(self, agents, replace=default_replace_vertex, replacements=None, info=None, delete_history=True):
        if replacements and info:
            for i, a in enumerate(agents):
                self.replace_vertex(a=a, replace=replace, replacement=replacements[i], info=info[i], delete_history=delete_history)
        elif replacements and not info:
            for i, a in enumerate(agents):
                self.replace_vertex(a=a, replace=replace, replacement=replacements[i], delete_history=delete_history)            
        else:
            for a in agents:
                self.replace_vertex(a=a, replace=replace, delete_history=delete_history)

    def update(self, f, t=-1):
        f(NW=self, t=t)

    def get_info(self):        
        self.info = {'count':{}}
        for a in self.get_vertices_iter():
            if a.name in self.info['count']:
                self.info['count'][a.name] += 1
            else:
                self.info['count'][a.name] = 1

        self.info['cc'] = "%.2f"%nx.average_clustering(self.G)
        return self.info

    def __str__(self):
        return str([v.name for v in self.G.nodes()]) +'\n' + str([(v1.name, v2.name) for (v1, v2) in self.G.edges()])

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

        for a in self.get_vertices_iter():
            colors.append(a.get_color())
            labels[a] = a.get_label()
        
        draw_graph(G=self.G, colors=colors, labels=labels, layout=LO)

    def print_edges(self):
        print [(a1.name, a2.name) for (a1, a2) in self.get_edges()]
        
    def print_vertices(self):
        print [v.name for v in self.get_vertices()]

    def print_nw(self):
        self.print_vertices()
        self.print_edges()

if __name__ == "__main__":
    nw = Network()
    nw.draw_NW()
    pause(5)