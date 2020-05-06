#!/usr/bin/env python3

import math

import sympy
from sympy import symbols as sym

def sign_var(s) :
	if s == 0.0 :
		return '0'
	else :
		return '+' if 0.0 < s else '-'

def compute_3(jm, am, a0, s0, sg, debug=False) :
	# calcul la commande en jrk nécessaire pour:
	#  * rejoindre la vitesse sg à partir de la vitesse s0
	#  * avec une accélération finale nulle

	J_m, A_m, A_0, S_0, S_g = sym('J_m A_m A_0 S_0 S_g')

	val = {
		'J_m': jm, 'A_m': am, 'A_0': a0, 'S_0': s0, 'S_g': sg,
	}

	# l'aire totale de l'accélération doit être égale au delta de vitesse
	Q_d = S_g - S_0

	if float(A_0.subs(val)) == 0.0 :
		# départ à accélération nulle
		s = math.copysign(1.0, sg - s0)

		Q_m = A_m ** 2 / J_m

		if float(abs(Q_d).subs(val)) <= float(Q_m.subs(val)) :
			# CASE 2
			# on a pas le temps d'atteindre l'accélération max
			# time_for_acc = math.sqrt(abs(aire_target) / jm)
			T_a = sympy.sqrt( abs(Q_d) / J_m )

			bch = "B" + sign_var(s)
			cmd = [s, -s]
			dur = [T_a, T_a]
		else :
			# CASE 1
			# on atteind l'accélération maximale
			# time_triangle = am / jm
			T_t = A_m / J_m
			# aire_restante_pour_rectangle = abs(aire_target) - aire_maxi_triangle
			Q_r = abs(Q_d) - Q_m
			# time_rectangle = aire_restante_pour_rectangle / am
			T_r = Q_r / A_m

			bch = "A" + sign_var(s)
			cmd = [s, 0, -s]
			dur = [T_t, T_r, T_t]
	else :
		# mais pour revenir à zero, il nous faut au moins un triangle, dont l'aire est égale à
		T_n = abs( A_0 ) / J_m
		Q_n = T_n * A_0 / 2
		Q_c = Q_d - Q_n

		s = math.copysign(1.0, a0)

		if 0 < float((Q_c * Q_n).subs(val)) :
			# l'aire restante est un triangle possiblement tronqué de taille maxi :
			Q_u = abs(A_m**2 - A_0**2) / ( J_m )
			if float(abs(Q_c).subs(val)) <= float(Q_u.subs(val)) :
				D = 4 * A_0**2 + 4 * J_m * abs(Q_c)
				T_b = (- 2 * abs(A_0) + sympy.sqrt(D) ) / ( 2 * J_m)

				bch = "C" + sign_var(s)
				cmd = [s, -s, -s]
				dur = [ T_b, T_b, T_n ]
			else :
				T_s = (abs(Q_c) - Q_u) / A_m

				bch = "D" + sign_var(s)
				cmd = [ s, 0, -s, -s]
				dur = [ abs(A_m - abs(A_0)) / J_m, T_s, abs(A_m - abs(A_0)) / J_m, T_n ]
			
		elif float((Q_c * Q_n).subs(val)) < 0 :
			# le reste n'est pas dans le même sens que le petit triangle
			# c'est un triangle et pas un trapèze, si l'aire restante est inférieure à :
			Q_s = A_m * A_m / J_m
			if float(Q_s.subs(val)) < float(abs(Q_c).subs(val)) :
				Q_g = abs(Q_c) - Q_s

				bch = "E" + sign_var(s)
				cmd = [ -s, -s, 0, s]
				dur = [ T_n, A_m / J_m, Q_g / A_m, A_m / J_m ]
			else :
				bch = "F" + sign_var(s)
				cmd = [ -s, -s, s]
				dur = [ T_n, sympy.sqrt(abs(Q_c) / J_m) , sympy.sqrt(abs(Q_c) / J_m) ]
		else :
			bch = "G0"
			cmd = [-s,]
			dur = [T_n,]

	return bch, cmd, dur, val

