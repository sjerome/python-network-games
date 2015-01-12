def payoff_creator(cc, cd, dd):
	(Ccc, Ccc) = cc
	(Ccd, Ddd) = cd
	(Ddd, Ddd) = dd
	def payoff(a1,a2,s):
		if s[a1] == 'C' and s[a2] == 'C':
			return {a1:Ccc, a2:Ccc}
		elif s[a1] == 'C' and s[a2] == 'D':
			return {a1:Ccd, a2:Dcd}
		elif s[a1] == 'D' and s[a2] == 'C':
			return {a1:Dcd, a2:Ccd}
		elif s[a1] == 'D' and s[a2] == 'D':
			return {a1:Ddd, a2:Ddd}
		else:
			return None
	return payoff
