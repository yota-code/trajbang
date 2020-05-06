#!/usr/bin/env python3

import collections
import random
import sys

from cc_pathlib import Path

from analytical import compute_3, sign_var
from plot import plot_3

test_vec = [
	[1.0, 1.0, 1.0, -0.5, 0.0],
	[1.0, 1.0, -0.5, 0.0, 0.5],
	[1.0, 1.0, 0.5, 0.0, 0.5],
	[1.0, 1.0, -0.5, 0.0, -0.5],
	[1.0, 1.0, 0.5, 0.0, -0.5],
	[1.0, 1.0, 0.0, 0.0, 0.5],
	[1.0, 1.0, 0.0, 0.0, -0.5],
	[1.0, 1.0, 0.0, 0.0, 2.0],
	[1.0, 1.0, 0.0, 0.0, -2.0],
	[1.0, 1.0, 0.75, 0.0, -2.0],
	[1.0, 1.0, -0.75, 0.0, 2.0],
	[1.0, 1.0, -0.25, 0.0, -2.0],
	[1.0, 1.0, 0.25, 0.0, 2.0],
]

test_cov = dict()

def test_val(jm, am, a0, s0, sg) :
	bch, cmd, dur, val = compute_3(jm, am, a0, s0, sg)

	if bch not in test_cov :
		test_cov[bch] = [cmd, dur]
		plot_3(cmd + [0.0,], [float(d.subs(val)) for d in dur] + [1.0,], val, bch)

for line in test_vec :
	test_val(* line)

while len(test_cov) < 13 :
	jm = random.randint(1, 200)
	am = random.randint(1, 400)
	if random.randrange(8) == 0 :
		a0 = 0
	else :
		a0 = random.randint(-am, am)
	s0 = random.randint(-400, 400)
	if random.randrange(8) == 0 :
		sg = s0
	else :
		sg = random.randint(-400, 400)
	jm, am, a0, s0, sg = [i / 20.0 for i in [jm, am, a0, s0, sg]]

	test_val(jm, am, a0, s0, sg)

for key in sorted(test_cov) :
	cmd, dur = test_cov[key]
	print(f"===  {key}  ===")
	for c, d in zip(cmd, dur) :
		print(f" {sign_var(c)}\t{d.expand()}")
