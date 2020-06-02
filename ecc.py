from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import HMAC, SHA256, SHA512
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Points import inverse_mod

from utils import *



def ECDH(d, H, parameters):
	(p, a, b, G, n, h) = parameters
	curve = (p, a, b)
	S = H * d
	return S

def ECDSA_sign(d, z, parameters):
	(p, a, b, G, n, h) = parameters
	curve = (p, a, b)
	k = random.randrange(1, n-1)
	P = G * k
	Px, Py = P.x, P.y
	r = Px % n
	while r == 0 or (z + r * d) % n == 0:
		k = random.randrange(1, n-1)
		P = G * k
		Px, Py = P.x, P.y
		r = Px % n
	s = (inverse_mod(k, n) * (z + r * d)) % n
	while s == 0:
		k = random.randrange(1, n-1)
		s = (inverse_mod(k, n) * (z + r * d)) % n

	return r, s

def ECDSA_verify(H, z, r, s, parameters):
	(p, a, b, G, n, h) = parameters
	curve = (p, a, b)
	u1 = (inverse_mod(s, n) * z) % n
	u2 = (inverse_mod(s, n) * r) % n
	P = (G * u1) + (H * u2)
	return (r % n )== (P.x % n)

def ECDSA_fixed_k(k, d, z, parameters):
	(p, a, b, G, n, h) = parameters
	curve = (p, a, b)
	P = G * k
	Px, Py = P.x, P.y
	r = Px % n
	s = (inverse_mod(k, n) * (z + r * d)) % n
	return r, s

def ECDSA_hack(z1, r1, s1, z2, r2, s2, n):
	k = ((z1 - z2) * inverse_mod(s1 - s2, n)) % n
	d = (inverse_mod(r1, n) * (s1 * k - z1)) % n
	return hex(d)


def ECIES_Encrypt(m, Kb, parameters):
	(p, a, b, G, n, h) = parameters
	r = random.randrange(1, n)
	R = G * r
	P = Kb * r
	Px, Py = P.x, P.y
	S = Px.to_bytes(64, 'big')
	salt = get_random_bytes(16)
	keys = PBKDF2(S, salt, 64, count=1000000, hmac_hash_module=SHA512)
	ke = keys[:32]
	km = keys[32:]

	cipher = AES.new(ke, AES.MODE_CBC)
	iv = cipher.iv
	m = pad(m, 32)
	c = cipher.encrypt(m)

	d = HMAC.new(km, c, digestmod=SHA256)

	return (R, c, d, salt, iv)


def ECIES_Decrypt(R, c, returned_d, salt, iv, d, parameters):
	(p, a, b, G, n, h) = parameters
	P = R * d
	Px, Py = P.x, P.y
	S = Px.to_bytes(64, 'big')
	keys = PBKDF2(S, salt, 64, count=1000000, hmac_hash_module=SHA512)
	ke = keys[:32]
	km = keys[32:]
	generated_h = HMAC.new(km, c, digestmod=SHA256)
	cipher = AES.new(ke, AES.MODE_CBC, iv)
	msg = cipher.decrypt(c)
	msg = unpad(msg, 32)
	return msg


































