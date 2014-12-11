deaths = set([])

def get_deaths():
	return deaths

def set_deaths(set_of_deaths):
	global deaths
	deaths = set_of_deaths

def remove_death(a):
	global deaths
	if a in deaths:
		deaths.remove(a)

def remove_deaths(agents):
	for a in agents:
		remove_death(a)

def clear_deaths():
	global deaths
	deaths = set([])

def add_death(agent):
	deaths.add(agent)