from Agent import Agent
import random 

def FM_should_add(self, other_agent, cost=0):
	p = self.get_info()['p']
	return random.random() > 7.0/(7.0+p) and\
		   (self != other_agent and\
		    (not self.get_history(other_agent=other_agent).get('actions') or\
		    self.get_history(other_agent=other_agent)['actions'][0][1] == 'C'))
