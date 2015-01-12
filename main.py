 # -*- coding: utf-8 -*-
from Simulation.Simulations import *
from Agent.Agents import *
import pylab as plt
import itertools
from statistics import mean, median, mode, stdev


draw_scale = 30
print_scale = draw_scale
# One of these should always be 1
play_scale = 1
rewire_scale = 1
log_scale = 1

if __name__ == "__main__":
	sim = FM(N=20)
	N = 1
	information = {'times':[]}
	for i in xrange(N):
		peoples = {}
		cc = []
		ps = []
		for t in xrange(2000): #itertools.count(0):
			if t % play_scale == 0:
				sim.play(t=t)

			if t % rewire_scale == 0:
				sim.rewire(t=t)

			if t % draw_scale == 0:
				plt.figure(0)
				sim.draw(t=t)

			if t % print_scale == 0:
				info = sim.get_info()
				counts = info['agent_information']['count']
				for (k, v) in counts.items():
					if k not in peoples:
						peoples[k] = ([t], [v])
					else:
						(times, cnt) = peoples[k]
						cnt.append(v)
						times.append(t)

				cc.append(info['cc'])

				pees = info['agent_information']['p']
				ps.append(mean(reduce(lambda x,y: x+y,pees.values())))
				# cs.append(info['agent_information']['count']['C'] if 'C' in info['agent_information']['count'] else 0)
				# ds.append(info['agent_information']['count']['D'] if 'D' in info['agent_information']['count'] else 0)

				# plt.figure(1)
				# plt.clf()
				# ps = info['agent_information']['p']
				# plt.boxplot(x=ps.values(), labels=ps.keys(), showmeans=True)
				# plt.draw()
				# plt.figure(1)

				# print info['agent_information']['count'], info['cc'],mean(reduce(lambda x,y: x+y,ps.values())),  str(t)

		plt.close()
		for (k, v) in peoples.items():
			if k == 'C':
				c = 'b'
			elif k == 'D':
				c = 'r'
			else:
				c = 'g'
			plt.plot(*v, color=c, label=k)
		plt.legend()
		plt.xlabel('t')
		plt.ylabel('Population')
		plt.show()
		raw_input()
		plt.close()
		plt.plot(cc, label='C.C.')
		plt.legend()
		plt.xlabel('t')
		plt.ylabel('Clustering Coefficient')
		plt.show()
		raw_input()
		plt.close()
		plt.plot(ps)
		plt.legend()
		plt.xlabel('t')
		plt.ylabel('Average P')
		plt.show()
		raw_input()

