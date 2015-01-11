 # -*- coding: utf-8 -*-
from Simulation.Simulations import *
from Agent.Agents import *
import pylab as plt
import itertools
from statistics import mean, median, mode, stdev


draw_scale = 50
print_scale = draw_scale
# One of these should always be 1
play_scale = 1
rewire_scale = 1

if __name__ == "__main__":
	sim = FM(N=20)

	for t in itertools.count(0):
		if t % play_scale == 0:
			sim.play(t=t)

		if t % rewire_scale == 0:
			sim.rewire(t=t)

		if t % draw_scale == 0:
			plt.figure(0)
			sim.draw(t=t)

		if t % print_scale == 0:
			info = sim.get_info()
			plt.figure(1)
			plt.clf()
			ps = info['agent_information']['p']
			plt.boxplot(x=ps.values(), labels=ps.keys(), showmeans=True	)
			plt.draw()
			plt.figure(1)

			print info['agent_information']['count'], info['cc'],mean(reduce(lambda x,y: x+y,ps.values())),  str(t)
