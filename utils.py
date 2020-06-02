import numpy as np
import random
import secrets
from Crypto.Hash import HMAC, SHA256, SHA512
import json
from Points import Point


def is_on_curve(P, a, b, p):
	"""
	Returns True if P is on the curve given by (a, b, p)
	"""
	x, y = P
	return ((y ** 2) % p) == ((x ** 3 + a * x + b) % p)

def hash_message(message, n):
	hash_object = SHA256.new(data=message)
	z = int.from_bytes(hash_object.digest(), 'big')
	z =  (int(bin(z)[:len(bin(n))], 2))
	return z


def power(x, y, m) :
	"""
	Returns x ^ y (mod m)
	"""
	if (y == 0) : 
		return 1
	p = power(x, y // 2, m) % m 
	p = (p * p) % m	 
	if(y % 2 == 0) : 
		return p	
	else :	
		return ((x * p) % m) 

def inverse_mod(x, p):
	"""
	Returns x ^ -1 (mod p)
	"""
	return power(x, p-2, p)


def naive_count_points(p, curve):
	"""
	Return N, the number of points on curve (a, b)
	"""
	a, b = curve
	results = 0
	x_2s = dict()
	for x in range(p):
		x_2 =(x ** 2) % p
		if x_2 not in x_2s:
			x_2s[x_2] = []
		x_2s[x_2].append(x)

	for x in range(p):
		y_2 = (x ** 3 + a * x + b) % p
		if y_2 in x_2s:
			ys = x_2s[y_2]
			results += len(ys)
	return results + 1 # plus inifinity point



def is_prime(n):
	if n == 0 or n == 1:
		return False
	if n == 2:
		return True
	for i in range(2, int(n ** 0.5) + 2):
		if n % i == 0:
			return False
	return True


def find_random_point(parameters):
	"""
	Return a random point P on the curve
	"""
	p, a, b = parameters
	possible_points = set()
	for i in range(p):
		y2 = (i ** 3 + a * i + b) % p
		for j in range(p):
			if (j ** 2) % p == y2:
				possible_points.add((i, j))
	P = secrets.choice(list(possible_points))
	return Point(P[0], P[1], (p, a, b))


def generate_curve(p):
	"""
	Generate a valid Elliptic Curve
	"""
	a = random.randint(-20, 20)
	b = random.randint(-20, 20)
	while (4 * a ** 3 + 27 * b ** 2) % p == 0:
		a = random.randint(-5, 5)
		b = random.randint(-5, 5)

	# Step 1
	N = naive_count_points(p, (a, b))
	prime_factors = []
	for i in range(2, N+1):
		if N % i == 0 and is_prime(i):
			prime_factors.append(i)

	# Step 2
	n = (prime_factors[-1])
	assert (is_prime(n))

	# Step 3
	h = int(N / n)

	# Step 4
	P = find_random_point((p, a, b))
	
	# Step 5
	G = P * h 	

 	# Step 6
	while (G.x, G.y) == (float('inf'), float('inf')):
		print (G, P)
		P = find_random_point((p, a, b))
		G = P * h
 
	return a, b, G, n, h

def generate_keys(parameters):
	"""
	Generate a public-private key pair (d, h) where h = dG
	"""
	(p, a, b, G, n, h) = parameters
	curve = (p, a, b)
	d = random.randrange(1, n)
	h = G * d
	while (h.x, h.y) == (float('inf'), float('inf')):
		d = random.randrange(1, n)
		h = G * d
	return d, h

def build_known_curves():	
	"""
	Load some know curves, i.e. secp256k1
	"""
	with open("known_curves.json", 'r') as f:
		data = json.load(f)
	curves = dict()
	for curve in data['curves']:
		name = curve['name']
		curves[name] = (int(curve['p'], 16), curve['a'], curve['b'], Point(int(curve['G'][0], 16), int(curve['G'][1], 16), (int(curve['p'], 16), curve['a'], curve['b'])), int(curve['n'], 16), curve['h'])
	return curves
