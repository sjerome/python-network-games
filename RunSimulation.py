 # -*- coding: utf-8 -*-
from Simulations import *
from Agents import *
import pylab as plt
import itertools


draw_scale = 50
print_scale = draw_scale
# One of these should always be 1
play_scale = 1
rewire_scale = 1

if __name__ == "__main__":
	sim = DNWDP(N=20)

	for t in itertools.count(0):
		if t % play_scale == 0:
			sim.play(t=t)

		if t % rewire_scale == 0:
			sim.rewire(t=t)

		if t % draw_scale == 0:
			sim.draw(t=t)

		if t % print_scale == 0:
			print sim.get_info(), str(t)