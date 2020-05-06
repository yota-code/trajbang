#!/usr/bin/env python3

import math

import numpy as np
import matplotlib.pyplot as plt

import sympy
from sympy import symbols as sym

from cc_pathlib import Path

def symbolic_equation_3(n=3) :

	T = sym(' '.join(f"T_{i}" for i in range(n)))
	J = sym(' '.join(f"J_{i}" for i in range(n)))
	
	A = [sym('A_0'),]
	for i in range(n) :
		A.append( A[-1] + J[i] * T[i] )
		
	S = [sym('S_0'),]
	for i in range(n):
		S.append( S[-1] + A[i] * T[i] + J[i] * T[i]**2 / 2 )
		
	return T, J, A, S


def check_target(exp, val) :
	try :
		assert( math.isclose(float(exp), float(val), rel_tol=1e-5, abs_tol=1e-5) )
		return "OK"
	except AssertionError :
		return f"[{exp} # {val}]"

def plot_3(c, d, val, prefix="check/") :

	# on recopie val
	val = {k : v for k, v in val.items()}
	
	n = len(c)

	T, J, A, S = symbolic_equation_3(n)

	print("d = ", d)
	t = np.cumsum([0.0,] + d)
	print("t = ", t)
	z = [float(i * val['J_m']) for i in c]
	print("z = ", z)

	for i in range(n) :
		val[f"T_{i}"] = d[i]
		val[f"J_{i}"] = z[i]
		
	t_xx = [
		np.linspace(t[i], t[i+1], 50)
		for i in range(n)
	]
	
	plt.figure(figsize=(8.27, 11.69))

	title = f"jm={val['J_m']}, am={val['A_m']}, a0={val['A_0']}, s0={val['S_0']}, sg={val['S_g']}"

	###  jerk  ###
	plt.subplot(3, 1, 1)
	j_xx = [
		( np.ones_like(t_xx[0]) * z[i] )
		for i in range(n)
	]
	for i in range(n) :
		plt.plot([t_xx[i][0],] + list(t_xx[i]) + [t_xx[i][-1],], [0.0,] + list(j_xx[i]) + [0.0,])
	plt.grid()
	plt.title(title)
	plt.ylabel("jerk")
	
	###  acceleration  ###
	plt.subplot(3, 1, 2)
	a_xx = list()
	for i in range(n) :
		a_xx.append(
			(a_xx[-1][-1] if a_xx else val['A_0']) + (t_xx[i] - t[i]) * j_xx[i][0]
		)

	for i in range(n) :
		plt.plot(t_xx[i], a_xx[i])
	a_lst = [i.subs(val) for i in A]
	plt.plot(t, a_lst, 'o', color="grey")
	plt.grid()
	plt.ylabel("acceleration")
	print("acc:", ', '.join(f'{round(float(i), 5):8.5f}' for i in a_lst))
	
	###  speed  ###
	plt.subplot(3, 1, 3)
	s_xx = list()
	for i in range(n) :
		s_xx.append(
			( s_xx[-1][-1] if s_xx else val['S_0'] ) +
			( a_xx[i][0] * (t_xx[i] - t[i]) ) +
			( j_xx[i][0] * (t_xx[i] - t[i])**2 / 2.0 )
		)

	for i in range(n) :
		plt.plot(t_xx[i], s_xx[i])
	s_lst = [i.subs(val) for i in S]
	plt.plot(t, s_lst, 'o', color="grey")
	plt.grid()
	plt.ylabel("speed")
	print("spd:", ', '.join(f'{round(float(i), 5):8.5f}' for i in s_lst))

	if prefix :
		check_sg, check_ag = check_target(s_lst[-1], val['S_g']), check_target(a_lst[-1], 0.0)
		#if check_sg != "OK" or check_ag != "OK" :
		Path("check").make_dirs()
		plt.savefig(f"check/{prefix}.compute_3({title}).{check_sg}.{check_ag}.png")
	else :
		plt.show()	

	return a_lst, s_lst