from Agent import Agent
from Behaviors import *
from Labels import *
from Addings import *
import random

def cooperator():
	return Agent(name='C', behavior=cooperate)

def defector():
	return Agent(name='D', behavior=defect)

def TFT():
	return Agent(name='TFT', behavior=tft)

def cooperator_with_mistakes(p=.1):
	def behavior(self, other_agent):
		return ('D' if random.random() < p else 'C')
	
	return Agent(name='CM', behavior=behavior)

def defector_with_mistakes(p=.1):
	def behavior(self, other_agent):
		return ('C' if random.random() < p else 'D')
	
	return Agent(name='CM', behavior=behavior)

def FM_agent_cooperator(p=None):
	return Agent(name='C', plot_color='b', kind=0, label=get_label_with_p, behavior=cooperate, should_add=FM_should_add, info={'p':p or max(0, random.gauss(.5, .4))})

def FM_agent_defector(p=None):
	return Agent(name='D', kind=1, plot_color='r', label=get_label_with_p, behavior=defect, should_add=FM_should_add, info={'p':p or max(0, random.gauss(.5, .4))})

def FM_agent_cooperator_S(p=None):
	return Agent(name='CS', kind=0, label=get_label_with_p, behavior=cooperate, should_add=FM_S_should_add, info={'p':p or max(0, random.gauss(0, 2))})

def FM_agent_defector_S(p=None):
	return Agent(name='DS', kind=1, label=get_label_with_p, behavior=defect, should_add=FM_S_should_add, info={'p':p or max(0, random.gauss(0, 2))})


# Random agents
def random_agent(types=None):
	types = types or [TFT, cooperator, defector]
	return random.choice(types)()

def coooperator_or_defector():
	return random_agent([cooperator, defector])

def FM_cooperator_or_defector():
	return random_agent([FM_agent_cooperator, FM_agent_defector])
