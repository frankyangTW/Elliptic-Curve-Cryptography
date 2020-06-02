
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

class Point:
	def __init__(self, x, y, curve):
		self.x = x
		self.y = y
		self.curve = curve # (p, a, b)

	def __str__(self):
		return "({}, {})".format(hex(self.x), hex(self.y))

	def __add__(self, Q):
		"""
		Return P + Q on the curve given by (p, a, b)
		"""
		# Define point of infinity to be (inf, inf)
		(p, a, b) = self.curve
		P = self
		# P + 0 = P, Q + 0 = Q
		if P.x == float('inf'):
			return Point(Q.x, Q.y, self.curve)
		if Q.x == float('inf'):
			return Point(P.x, P.y, self.curve)
		# P + (-P) = 0
		if ((P.x % p) == (Q.x % p)) and (P.y + Q.y) % p == 0:
			return Point(float('inf'), float('inf'), self.curve)
		# P = Q
		if P.x == Q.x and P.y == Q.y:
			m = ((3 * P.x ** 2 + a)*(inverse_mod(2 * P.y, p))) % p
		# P != Q
		else:
			m = ((P.y - Q.y) * (inverse_mod(P.x-Q.x, p))) % p
		xr = (m ** 2 - P.x - Q.x) % p
		yr = (P.y + m * (xr - P.x)) % p
		return Point(xr, -yr % p, self.curve)

	def __mul__(self, n):
		P = Point(self.x, self.y, self.curve)
		s = Point(float('inf'), float('inf'), self.curve)
		bin_n = str(bin(n))[2:][::-1]
		for d in bin_n:
			if d == '1':
				s = s + P
			P = P + P
		return s

	def __eq__(self, Q):
		return self.x == Q.x and self.y == Q.y







