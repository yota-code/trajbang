#!/usr/bin/env python3

def _bezier_pascal_coef(n) :
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
	
def _bezier_print_polynoms(n) :
	""" this is to prepare the polynoms for mathematica which is shit """
	t0 = [(f't^{i}' if i != 0 else None) for i in range(n)]
	t1 = [(f'(1-t)^{n-i-1}' if n-i-1 != 0 else None) for i in range(n)]
	c = [(str(i) if i != 1 else None) for i in _bezier_pascal_coef(n)]
	px = [f'p{i}x' for i in range(n)]
	py = [f'p{i}y' for i in range(n)]
	
	print(t0)
	print(t1)

	print('x[t_] := ' + ' + '.join('*'.join([i for i in m if i is not None]) for m in zip(px, c, t0, t1)))
	print('y[t_] := ' + ' + '.join('*'.join([i for i in m if i is not None]) for m in zip(py, c, t0, t1)))

	

if __name__ == '__main__' :
	
	for i in range(1, 10) :
		print(i, _bezier_pascal_coef(i))

	_bezier_print_polynoms(8)
