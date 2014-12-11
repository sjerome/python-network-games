from Agent import Agent
from Behaviors import *
import random


def cooperator():
	return Agent(name='C', behavior=cooperate)

def defector():
	return Agent(name='D', behavior=defect)

def TFT():
	def behavior(self, other_agent):
		action_list = self.get_history(other_agent).get('actions')
		if action_list == None:
			return 'C'
		else:
			return action_list[-1][1]
	return Agent(name='TFT', behavior=behavior)

def cooperator_with_mistakes(p=.1):
	def behavior(self, other_agent):
		return ('D' if random.random() < p else 'C')
	
	return Agent(name='CM', behavior=behavior)

def defector_with_mistakes(p=.1):
	def behavior(self, other_agent):
		return ('C' if random.random() < p else 'D')
	
	return Agent(name='CM', behavior=behavior)

def pTFT(p=.5):
	def behavior(self, other_agent):
		action_list = self.get_history(other_agent).get('actions')
		if action_list == None:
			return 'C'

		c = 0
		d = 0
		for i in action_list:
			if i[1] == 'C':
				c += 1
			else:
				d += 1
		if c + d == 0:
			return 'C'

		if float(c)/float(c+d) >= p:
			return 'C'

		return 'D'

	return Agent(name='H', behavior=behavior)

def FM_agent_cooperator(p=.5):
	def should_add(self, other_agent, cost):
		if other_agent.get_kind() < .2:
			return True
		return False
	def should_remove(self, other_agent, cost):
		if other_agent.get_kind() < .2:
			return False
		return True
	return Agent(name='FMC', kind=0, behavior=cooperate, should_add=should_add, should_remove=should_remove, info={'p':p})

def FM_agent_defector(p=.5):
	def should_add(self, other_agent, cost):
		if other_agent.get_kind() < .2:
			return True
		return False
	def should_remove(self, other_agent, cost):
		if other_agent.get_kind() < .2:
			return False
		return True
	return Agent(name='FMD', kind=1, behavior=defect, should_add=should_add, should_remove=should_remove, info={'p':p})

# Random agents
def random_agent(types=None):
	types = types or [TFT, cooperator, defector]
	return random.choice(types)()

def coooperator_or_defector():
	return random_agent([cooperator, defector])
