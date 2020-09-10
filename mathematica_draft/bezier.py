#!/usr/bin/env python3

import math

import numpy as np
import matplotlib.pyplot as plt

import sympy
from sympy import symbols as sym

t = sym('t')

class Bezier() :
	def __init__(self, arg=None) :

		self.p_lst = None
		if arg is None :
			self.n = None

		try :
			self.set_p(arg)
		except TypeError :
			self.n = int(arg)

	def set_p(self, p_lst) :
		self.p_lst = list(p_lst)
		self.n = len(p_lst)

		self.val = dict()
		for i, (a, b) in enumerate(self.p_lst) :
			self.val[f'P^{i}_x'] = a
			self.val[f'P^{i}_y'] = b

	def p_coef(self, n) :
		if n <= 0 :
			raise ValueError("n must be in N*")
		q_lst = [1,]
		for i in range(n-1) :
			r_lst = [1,]
			for a, b in zip(q_lst[:-1], q_lst[1:]) :
				r_lst.append(a + b)
			r_lst.append(1)
			q_lst = r_lst
		return q_lst

	def get_sympy(self) :

		n = self.n

		px_lst = sym(' '.join(f'P^{i}_x' for i in range(n)))
		py_lst = sym(' '.join(f'P^{i}_y' for i in range(n)))

		q_lst = self.p_coef(n)

		x0 = 0
		y0 = 0
		for i in range(n) :
			x0 += q_lst[i] * px_lst[i] * (t)**i * (1-t)**(n-i-1)
			y0 += q_lst[i] * py_lst[i] * (t)**i * (1-t)**(n-i-1)

		x1 = sympy.diff(x0, t)
		y1 = sympy.diff(y0, t)
		x2 = sympy.diff(x1, t)
		y2 = sympy.diff(y1, t)

		s0 = (x1*y2 - y1*x2) / ( x1**2 + y1**2 )**sympy.Rational(3,2)

		return x0, y0, s0

	def print_wolfram(self) :
		""" this is to prepare the polynoms for mathematica, which is unable to do it himself easily """

		n = self.n

		t0 = [(f't^{i}' if i != 0 else None) for i in range(n)]
		t1 = [(f'(1-t)^{n-i-1}' if n-i-1 != 0 else None) for i in range(n)]
		c = [(str(i) if i != 1 else None) for i in self.p_coef(n)]

		px = [f'p{i}x' for i in range(n)]
		py = [f'p{i}y' for i in range(n)]

		print('x[t_] := ' + ' + '.join('*'.join([i for i in m if i is not None]) for m in zip(px, c, t0, t1)))
		print('y[t_] := ' + ' + '.join('*'.join([i for i in m if i is not None]) for m in zip(py, c, t0, t1)))
		print("s[t_] := (x'[t]*y''[t] - y'[t]*x''[t]) / (( x'[t]^2 + y'[t]^2 )^(3/2))")

	def plot(self, p_lst=None) :
		if p_lst is not None :
			self.set_p(p_lst)

		t_lst = np.linspace(0, 1.0, 100)

		x0, y0, s0 = self.get_sympy()

		s1 = sympy.diff(s0, t)
		s2 = sympy.diff(s1, t)

		x0_lst = [float(x0.subs(self.val).subs({'t': i})) for i in t_lst]
		y0_lst = [float(y0.subs(self.val).subs({'t': i})) for i in t_lst]
		
		s0_val = s0.subs(self.val)
		s0_lst = [float(s0_val.subs({'t': i})) for i in t_lst]
		s1_val = s1.subs(self.val)
		s1_lst = [float(s1_val.subs({'t': i})) for i in t_lst]
		s2_val = s2.subs(self.val)
		s2_lst = [float(s2_val.subs({'t': i})) for i in t_lst]
		
		fig = plt.figure(figsize=(18, 16), dpi= 80, facecolor='w', edgecolor='k')
		
		plt.subplot(3,1,1)
		plt.axis("equal")
		plt.plot(
			[a for a, b in self.p_lst],
			[b for a, b in self.p_lst],
		'o-')
		plt.plot(x0_lst, y0_lst)	
		plt.subplot(3,1,2)
		plt.title("curvature")
		plt.plot(t_lst, s0_lst)
		plt.subplot(3,1,3)
		plt.title("first and second order derivative of the curvature")
		plt.plot(t_lst, s1_lst)
		# plt.plot(t_lst, s2_lst)
		# plt.subplot(4,1,4)
		# plt.title("second order derivative of the curvature")

		plt.show()

def curve_to_line(d, r0, p4, p7) :
	u = Bezier(8)
	a1 = math.asin( 7*d*r0 / 6)
	a2 = -a1 + math.asin((7*d*(-8*r0 + 3*r0*math.sqrt(36 - 49*d**2*r0**2)))/30)
	p_lst = [
		(0, 0), (d, 0), (d + d*math.cos(a1), d*math.sin(a1)), (d + d*math.cos(a1) + d*math.cos(a1+a2), d*math.sin(a1) + d*math.sin(a1+a2)),
		p4, ( (2*p4[0] + p7[0])/3, (2*p4[1] + p7[1])/3 ),( (p4[0] + 2*p7[0])/3, (p4[1] + 2*p7[1])/3 ), p7
	]
	u.plot(p_lst)

if __name__ == '__main__' :

	curve_to_line(1, -0.5, (5, 5), (7, 7))
	
