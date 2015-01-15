from Agent import Agent
import random 

def FM_should_add(self, other_agent, cost=0):
	p = self.get_info()['p']
	return self != other_agent and not self.was_defected_by(other_agent=other_agent)

def FM_S_should_add(self, other_agent, cost=0):
	p = self.get_info()['p']
	if other_agent.get_behavior(other_agent=self) == 'D':
		return False
	else:
		return FM_should_add(self=self, other_agent=other_agent, cost=0)


def SM_should_add(self, other_agent, cost=0):
	p = self.get_info()['p']
	return random.random() < p and self != other_agent and not self.was_defected_by(other_agent)