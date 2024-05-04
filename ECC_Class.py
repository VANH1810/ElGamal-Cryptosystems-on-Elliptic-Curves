import hashlib
import random
import math
import warnings


block_size = 2


def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - y * (a // b)
def mod_inverse(e, phi_n):
    gcd, x, y = extended_gcd(e, phi_n)
    if gcd != 1:
        raise ValueError("e doesn't have inverse module phi_n")
    else:
        return x % phi_n
def generate_prvKey(bits):
    return random.getrandbits(bits)
    
class Elliptic_Curves:
    def __init__(self, a, b, field, name):
        self.name = name
        self.a = a
        self.b = b
        self.field = field
        self.g = Point(self, self.field.g[0], self.field.g[1])
        
    def is_singular(self):
        return (4 * self.a**3 + 27 * self.b**2) % self.field.p == 0

    def on_curve(self, x, y):
        return (y**2 - x**3 - self.a * x - self.b) % self.field.p == 0

    def __eq__(self, other):
        if not isinstance(other, Elliptic_Curves):
            return False
        return self.a == other.a and self.b == other.b and self.field == other.field

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "\"%s\" => y^2 = x^3 + %dx + %d (mod %d)" % (self.name, self.a, self.b, self.field.p)

class Point:
    
    def __init__(self, curve, x, y):
        self.curve = curve
        self.x = x
        self.y = y
        self.p = self.curve.field.p
        self.on_curve = True
        if not self.curve.on_curve(self.x, self.y):
            warnings.warn("Point (%d, %d) is not on curve \"%s\"" % (self.x, self.y, self.curve))
            self.on_curve = False

    def __eq__(self, other_point):
        if not isinstance(other_point, Point):
            return False
        return self.x == other_point.x and self.y == other_point.y and self.curve == other_point.curve

    def __ne__(self, other_point):
        return not self.__eq__(other_point)
    
    def __str__(self):
        return "(%d, %d) %s %s" % (self.x, self.y, "on" if self.on_curve else "off", self.curve)

    def __repr__(self):
        return self.__str__()
    
    def ECdouble(self):
        a_curve = self.curve.a
        x1, y1 = self.x, self.y
        slope = (3 * x1 * x1 + a_curve) * pow(2 * y1, -1, self.p) % self.p
        x3 = (slope * slope - 2 * x1) % self.p
        y3 = (slope * (x1 - x3) - y1) % self.p  
        return Point(self.curve, x3, y3)

    def ECadd_point(self, other_point):
        if isinstance(other_point, Point):
            if self == other_point:
                return self.ECdouble()
            if self.curve == other_point.curve:
                a_curve = self.curve.a
                x1, y1 = self.x, self.y
                x2, y2 = other_point.x, other_point.y
                
                slope = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p
                x3 = (slope * slope - x1 - x2) % self.p
                y3 = (slope * (x1 - x3) - y1) % self.p
                return Point(self.curve, x3, y3)
            else:
                raise ValueError("Points are not on the same curve")
        else:
            raise TypeError("Unsupported operand type(s) for +: '%s' and '%s'" % (other_point.__class__.__name__,
                                                                                  self.__class__.__name__))

    def ECmultiply(self, ScalarHex):
        if isinstance(ScalarHex, int):
            if ScalarHex == 0:
                return None
            
            Q = Point(self.curve, self.x, self.y)
            ScalarBin = bin(ScalarHex)[2:]
            for bit in ScalarBin[1:]:
                Q = Q.ECdouble()
                if bit == '1':
                    Q = Q.ECadd_point(self)
            return Q
        else:
            raise TypeError("Unsupported operand type(s) for *: '%s' and '%s'" % (ScalarHex.__class__.__name__,
                                                                                  self.__class__.__name__))
    
    
class KeyPair:
    def __init__(self, curve, priv=None, pub=None):
        if priv is None and pub is None:
            raise ValueError("Private and/or public key must be provided")
        self.curve = curve
        self.can_sign = True
        self.can_encrypt = True
        if priv is None:
            self.can_decrypt = False
        self.priv = priv
        self.pub = pub
        if pub is None:
            self.pub = self.curve.g.ECmultiply(self.priv)

class SubGroup:
    def __init__(self, p, g, n, h):
        self.p = p
        self.g = g
        self.n = n
        self.h = h

    def __eq__(self, other):
        if not isinstance(other, SubGroup):
            return False
        return self.p == other.p and self.g == other.g and self.n == other.n and self.h == other.h

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Subgroup => generator %s, order: %d, cofactor: %d on Field => prime %d" % (self.g, self.n,
                                                                                           self.h, self.p)
    def __repr__(self):
        return self.__str__()

class ECC:
    def __init__(self, curve, keypair=None):
        self.curve = curve
        self.keypair = keypair
        self.can_decrypt = True
        self.can_encrypt = True
        if keypair is None:
            self.can_sign = False
            self.can_encrypt = False
        elif keypair.priv is None:
            self.can_decrypt = False
        elif keypair.pub is None:
            self.can_encrypt = False

    def __eq__(self, other):
        if not isinstance(other, ECC):
            return False
        return self.curve == other.curve and self.keypair == other.keypair

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Elliptic Curve Cryptography => curve %s, keypair %s" % (self.curve, self.keypair)

    def __repr__(self):
        return self.__str__()

    def encrypt(self, k, message):
        if not self.can_encrypt:
            raise ValueError("No public key available for encryption")
        else:
            C1 = self.curve.g.ECmultiply(k)
            C2 = self.keypair.pub.ECmultiply(k)
            C2_str = f"{C2.x}{C2.y}"
            C2_hash = hashlib.sha256(C2_str.encode()).hexdigest()
            C2_int = int(C2_hash, 16) % self.curve.field.p

            # Convert plaintext to bytes
            message_bytes = message.encode()

            # Split plaintext into even blocks
            blocks = [message_bytes[i:i+block_size] for i in range(0, len(message_bytes), block_size)]
            ciphertext_blocks = []
            for block in blocks:
                block_int = int.from_bytes(block, byteorder='big')
                encrypted_block = (C2_int + block_int) % self.curve.field.p
                ciphertext_blocks.append(encrypted_block)
            ciphertext_str_blocks = [str(block) for block in ciphertext_blocks]

            ciphertext_str = ' '.join(ciphertext_str_blocks)
            
            return C1, ciphertext_str
        
    def decrypt(self, cipher):
        C1, ciphertext_str = cipher
        if not self.can_decrypt:
            raise ValueError("No private key available for decryption")
        else:
            point = C1.ECmultiply(self.keypair.priv)
            point_str = f"{point.x}{point.y}"
            point_hash = hashlib.sha256(point_str.encode()).hexdigest()
            point_int = int(point_hash, 16) % self.curve.field.p

            ciphertext = [int(block) for block in ciphertext_str.split()]
            decrypted_blocks = [((block - point_int + self.curve.field.p) % self.curve.field.p) for block in ciphertext]

            # Convert decrypted blocks to bytes and then to string
            decrypted_bytes = b''.join(block.to_bytes(block_size, 'big') for block in decrypted_blocks)

            plaintext = decrypted_bytes.decode('utf-8')

            return plaintext
            