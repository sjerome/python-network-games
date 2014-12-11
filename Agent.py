 # -*- coding: utf-8 -*-
import random 
import copy
import Event as zp

# Default Functions
def default_utility(self, other_agent, me, him):
	if me == 'C' and him == 'C':
		return .03
	elif me == 'C' and him == 'D':
		return -.03
	elif me == 'D' and him == 'C':
		return .05
	else:
		return 0.0

def default_get_behavior(self, other_agent):
	return 'C'

def default_get_label(a):
	return a.name + "%.2f"%a.get_fitness()

def default_should_add(self, other_agent, cost=0):
	if self != other_agent and (not self.get_history(other_agent).get('actions') or self.get_history(other_agent)['actions'][0][1] == 'C'):
		return True
	return False

def default_should_remove(self, other_agent, cost=0):
	if not self.get_history(other_agent).get('actions') or self.get_history(other_agent)['actions'][0][1] == 'C':
		return False
	return True

def default_get_child(self, new_name=None, kind=None, behavior=None, u=None, label=None, should_add=None, should_remove=None, fitness=None, child=None, update=None, tire=None, info=None):
	return Agent(name= (new_name or self.name), kind=(kind or self.type), behavior= (behavior or self.behavior), u= (u or self.U), label=(label or self.label), should_add = (should_add or self.would_add), should_remove=(should_remove or self.would_remove), fitness=(fitness or self.fitness), child = (child or self.child), update= (update or self.up), tire=(tire or self.step), info=(info or self.info))

def default_fitness(self, t=-1):
	return self.get_utility()

def default_update(self, s1, s2, a2, t=-1):
	self.set_utility(self.utility+self.U(self, other_agent=a2, me=s1, him=s2))

def default_step(self, t=-1):
	self.set_utility(self.utility)

# Agent object
class Agent:
	# Name is anything, just to help identify agent
	# kind is number between [0,1) to identify type
	# behavior is a function (H, a2)->action
	# utility is a function  (agent 1, agent 2, my action, his action)-> float
	# label is a function from agent->label
	# child is function (agent, info)->agent 
	# fitness (agent, t)-> double
	# update (a, s1, s2, a2, t)-> void
	# step self, t -> void
	def __init__(self, name='C', kind=.5, behavior=default_get_behavior, u=default_utility, label=default_get_label, should_add = default_should_add, should_remove = default_should_remove, fitness=default_fitness, child=default_get_child, update=default_update, tire=default_step, info=None):
		self.name = str(name)
		self.type = kind
		self.behavior = behavior
		self.U = u
		self.label = label
		self.would_add = should_add
		self.would_remove = should_remove
		self.fitness = fitness
		self.child = child
		self.up = update
		self.step = tire

		self.alive = True
		self.history = {}
		self.utility = .5
		self.info = copy.deepcopy(info) if info else {}


	def get_name(self):
		return self.name

	def get_kind(self):
		return self.type

	def get_behavior(self, other_agent):
		return self.behavior(self, other_agent)

	def get_all_history(self):
		return self.history

	def get_history(self, a2):
		if a2 not in self.history:
			return {}
		return self.history[a2]

	def get_utility(self):
		return self.utility

	def get_fitness(self, t=-1):
		return self.fitness(self, t)

	def get_info(self, t=-1):
		return self.info

	def get_label(self):
		return self.label(self)

	def get_color(self):
		n = self.get_fitness()
		R = (255 * (1 - n)) 
		G = (255 * (n))
		B = 0
		return (R/255.0,G/255.0,B/255.0)

	def has_died(self):
		return not self.alive

	def reset_utility(self):
		self.set_utility(.5)

	def set_utility(self, utility):
		if self.get_fitness(self) <= 0:
			self.alive = False

		self.utility = min(max(utility, 0), 1)

	def update_history(self, a2, s1, s2, t=-1):
		if a2 not in self.history:
			self.history[a2] = {'actions':[(s1, s2, t)]}
			return

		his = self.history[a2]['actions']
		his.append((s1, s2, t))

		if len(his) > 10:
			self.history[a2]['actions'] = his[1:]

	def update(self, s1, s2, a2, t=-1):
		self.update_history(a2=a2, s1=s1, s2=s2, t=t)
		self.up(self=self, s1=s1, s2=s2, a2=a2, t=t)

	def tire(self, t=-1):
		self.step(self=self, t=t)

	def removed_agent(self, other_agent):
		if other_agent in self.history:
			del self.history[other_agent]

	def removed_agents(self, other_agents):
		for a in other_agents:
			self.removed_agent(a)

	def should_add(self, other_agent, cost=0):
		return self.would_add(self, other_agent, cost)

	def should_remove(self, other_agent, cost=0):
		return self.would_remove(self, other_agent, cost)

	def morph_agent(self, other_agent, new_name=None, new_history=None, new_utility=.5, new_info=None, alive=True):
		self.name=new_name or other_agent.name
		self.type = other_agent.type
		self.behavior = other_agent.behavior
		self.U = other_agent.U
		self.label = other_agent.label
		self.would_add = other_agent.would_add
		self.would_remove = other_agent.would_remove
		self.fitness = other_agent.fitness
		self.child = other_agent.child
		self.info = new_info or copy.deepcopy(other_agent.info)

		self.history = new_history or {}
		self.utility = new_utility
		self.alive = alive

	def get_child(self, new_name=None, info=None):
		return self.child(self, new_name=new_name, info=info)

	def __str__(self):
		return str(self.name)

if __name__ == "__main__":
	a1 = Agent()
	a2 = Agent()
	print a1, a1.get_utility()
	print a2, a2.get_utility()