 # -*- coding: utf-8 -*-
from Agent import Agent

def cooperate(self, other_agent):
	return 'C'

def defect(self, other_agent):
	return 'D'

def tft(self, other_agent):
	action_list = self.get_history(other_agent).get('actions')
	return action_list[-1][1] if action_list else 'C'