 # -*- coding: utf-8 -*-
import random 
import copy

# Default Functions

# Default payoff...b=.05, c=.03
def default_payoff(a1, a2, s):
	if s[a1] == 'C' and s[a2] == 'C':
		return {a1:1, a2:1}
	elif s[a1] == 'C' and s[a2] == 'D':
		return {a1:-1, a2:2}
	elif s[a1] == 'D' and s[a2] == 'C':
		return {a1:2, a2:-1}
	elif s[a1] == 'D' and s[a2] == 'D':
		return {a1:-.3, a2:-.3}
	else:
		return None

def default_get_behavior(self, other_agent):
	return 'C'

def default_get_label(self):
	return self.name + "%.2f"%self.get_fitness()

def default_should_add(self, other_agent, cost=0):
	return (self != other_agent and (not self.get_history(other_agent=other_agent).get('actions') or\
		self.get_history(other_agent=other_agent)['actions'][0][1] == 'C'))

def default_should_remove(self, other_agent, cost=0):
	return not (not self.get_history(other_agent=other_agent).get('actions') or\
		self.get_history(other_agent=other_agent)['actions'][0][1] == 'C')

def default_get_child(self, name=None, kind=None, behavior=None, payoff=None, label=None, should_add=None,
	should_remove=None, fitness=None, child=None, update=None, tire=None, get_color=None, new_info=None,
	selection=None, plot_color=None):

	return Agent(name= (name or self.name), kind=(kind or self.type), behavior= (behavior or self.behavior),\
		payoff = (payoff or self.U), label=(label or self.label), should_add = (should_add or self.would_add),\
		should_remove=(should_remove or self.would_remove), fitness=(fitness or self.fitness),\
		child = (child or self.child), update= (update or self.up), tire=(tire or self.step),\
		info=(new_info or self.info), get_color=(get_color or self.color_func),\
		selection=(selection or self.selection), plot_color=(plot_color or self.plot_color))

def default_fitness(self, t=-1):
	return max(0.01, 1 + self.get_selection() * self.get_payoff())

def default_update(self, other_agent, s, t=-1):
	self.set_payoff(payoff=self.get_payoff()+self.U(a1=self, a2=other_agent, s=s)[self])

def default_step(self, t=-1):
	self.set_payoff(payoff=self.get_payoff()-.01)
	return

def default_get_color(self, avg=None, std=None, t=-1):
		avg = avg or 1
		std = 1 if not std or std == 0.0 else std
		normalized = (self.get_fitness() - avg)/(2.0*std) + .4
		n = min(max(normalized, 0), 1)
		R = (255 * (1 - n))
		G = (255 * (n))
		B = 0
		return (R/255.0, G/255.0, B/255.0)

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
	# info is a dictionary of important information about the agent
	# selection is how important the payoff is to a persons fitness, defined as 1+selection*payoff
	def __init__(self, name='C', kind=.5, behavior=default_get_behavior, payoff=default_payoff, 
		label=default_get_label, should_add = default_should_add, should_remove = default_should_remove,
		fitness=default_fitness, child=default_get_child, update=default_update, tire=default_step, get_color=default_get_color,
		info=None, selection=.08, plot_color='b'):

		self.name = str(name)
		self.type = kind
		self.behavior = behavior
		self.U = payoff
		self.label = label
		self.would_add = should_add
		self.would_remove = should_remove
		self.fitness = fitness
		self.child = child
		self.up = update
		self.step = tire
		self.color_func = get_color
		self.plot_color = plot_color

		self.alive = True
		self.history = {}
		self.total_payoff = 0.0
		self.info = copy.deepcopy(info) if info else {}
		self.selection=selection

	def get_name(self):
		return self.name

	def get_kind(self):
		return self.type

	def get_selection(self):
		return self.selection

	def get_behavior(self, other_agent):
		return self.behavior(self=self, other_agent=other_agent)

	def get_all_history(self):
		return self.history

	def get_history(self, other_agent):
		return {} if other_agent not in self.history else self.history[other_agent]

	def get_fitness(self, t=-1):
		return self.fitness(self=self, t=t)

	def get_info(self, t=-1):
		return self.info

	def get_label(self):
		return self.label(self=self)

	def get_color(self, avg=None, std=None, t=-1):
		return self.color_func(self=self, avg=avg, std=std, t=-1)

	def get_should_add_function(self):
		return self.would_add

	def get_should_remove_function(self):
		return self.would_remove

	def get_behavior_function(self):
		return self.behavior

	def get_plot_color(self):
		return self.plot_color

	## REALY SHOULD NEVER BE USED UNLESS FOR DEFINING FITNESS FUNCTION, USE FITNESS TO ABSTRACT UTILITY
	def get_payoff(self):
		return self.total_payoff

	def has_died(self):
		return not self.alive

	def is_alive(self):
		return self.alive

	def reset_utility(self):
		self.set_payoff(0.0)

	def set_payoff(self, payoff):
		self.total_payoff = payoff

		if self.get_fitness() <= 0:
			self.alive = False

	def update_history(self, other_agent, s={}, t=-1):
		if other_agent not in self.history:
			self.history[other_agent] = {'actions':[(s[self], s[other_agent], t)]}
			return

		his = self.history[other_agent]['actions']
		his.append((s[self], s[other_agent], t))

		if len(his) > 10:
			self.history[other_agent]['actions'] = his[1:]

	def update(self, other_agent, s={}, t=-1):
		self.update_history(other_agent=other_agent, s=s, t=t)
		self.up(self=self, other_agent=other_agent, s=s, t=t)

	def tire(self, t=-1):
		self.step(self=self, t=t)

	def removed_agent(self, other_agent):
		if other_agent in self.history:
			del self.history[other_agent]

	def removed_agents(self, other_agents):
		for a in other_agents:
			self.removed_agent(other_agent=a)

	def should_add(self, other_agent, cost=0):
		return self.would_add(self=self, other_agent=other_agent, cost=cost)

	def should_remove(self, other_agent, cost=0):
		return self.would_remove(self=self, other_agent=other_agent, cost=cost)

	def morph_agent(self, other_agent, new_name=None, new_history=None, new_payoff=0.0, new_info=None, alive=True):
		self.name=new_name or other_agent.name
		self.type = other_agent.type
		self.behavior = other_agent.behavior
		self.U = other_agent.U
		self.label = other_agent.label
		self.would_add = other_agent.would_add
		self.would_remove = other_agent.would_remove
		self.fitness = other_agent.fitness
		self.child = other_agent.child
		self.color_func = other_agent.color_func
		self.selection = other_agent.selection
		self.plot_color = other_agent.plot_color

		self.info = new_info or copy.deepcopy(other_agent.info)
		self.history = new_history or {}
		self.total_payoff = new_payoff
		self.alive = alive

	def get_child(self, name=None, kind=None, behavior=None, payoff=None, label=None,
	 should_add=None, should_remove=None, fitness=None, child=None, update=None, tire=None, 
	 get_color=None, new_info=None, selection=None):

		return self.child(self, name=name, kind=kind, behavior=behavior,
			payoff=payoff, label=label, should_add=should_add, should_remove=should_remove,
			fitness=fitness, child=child, update=update, tire=tire, get_color=get_color,
			new_info=new_info, selection=selection)

	def __str__(self):
		return str(self.name)

if __name__ == "__main__":
	a1 = Agent()
	a2 = Agent()
	a1.update(other_agent=a2, s={a1:a1.get_behavior(other_agent=a2), a2:a2.get_behavior(other_agent=a1)})
	a2.update(other_agent=a1, s={a1:a1.get_behavior(other_agent=a2), a2:a2.get_behavior(other_agent=a1)})

	print a1, a1.get_utility()
	print a2, a2.get_utility()

	a1.update(other_agent=a2, s={a1:a1.get_behavior(other_agent=a2), a2:a2.get_behavior(other_agent=a1)})
	a2.update(other_agent=a1, s={a1:a1.get_behavior(other_agent=a2), a2:a2.get_behavior(other_agent=a1)})

	print a1, a1.get_utility()
	print a2, a2.get_utility()