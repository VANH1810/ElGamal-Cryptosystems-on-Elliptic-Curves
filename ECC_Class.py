import hashlib
import random
import math
import warnings

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
    def __init__(self, curve, block_size, keypair=None):
        self.curve = curve
        self.keypair = keypair
        self.block_size = block_size

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

    def encrypt(self, publicKey, k , message):
       
            C1 = self.curve.g.ECmultiply(k)
            C2 = publicKey.ECmultiply(k)
            C2_str = f"{C2.x}{C2.y}"
            C2_hash = hashlib.sha256(C2_str.encode()).hexdigest()
            C2_int = int(C2_hash, 16) % self.curve.field.p

            # Convert plaintext to bytes
            message_bytes = message.encode()

            # Split plaintext into even blocks
            blocks = [message_bytes[i:i+self.block_size] for i in range(0, len(message_bytes), self.block_size)]
            ciphertext_blocks = []
            for block in blocks:
                block_int = int.from_bytes(block, byteorder='big')
                encrypted_block = (C2_int + block_int) % self.curve.field.p
                ciphertext_blocks.append(encrypted_block)
            ciphertext_str_blocks = [str(block) for block in ciphertext_blocks]

            ciphertext_str = ' '.join(ciphertext_str_blocks)
            
            with open('ECC - Encrypt and Decrypt/cipherText.txt', 'w') as file:
                # Write C1 and ciphertext_str to the file
                file.write(f"C1: {C1}\n")
                file.write(f"ciphertext_str: {ciphertext_str}\n")
            return C1, ciphertext_str
        
    def decrypt(self, privateKey, cipher):
        C1, ciphertext_str = cipher
        point = C1.ECmultiply(privateKey)
        point_str = f"{point.x}{point.y}"
        point_hash = hashlib.sha256(point_str.encode()).hexdigest()
        point_int = int(point_hash, 16) % self.curve.field.p

        ciphertext = [int(block) for block in ciphertext_str]
        decrypted_blocks = [((block - point_int + self.curve.field.p) % self.curve.field.p) for block in ciphertext]

        # Convert decrypted blocks to bytes
        decrypted_bytes = b''.join(block.to_bytes(self.block_size, 'big') for block in decrypted_blocks)

        # Convert to string
        plaintext = decrypted_bytes.decode('utf-8')

        # Remove NULL bytes before the last character
        if len(plaintext) > 1 and plaintext[-2] == '\x00':
            plaintext = plaintext[:-2] + plaintext[-1]

        with open('ECC - Encrypt and Decrypt/decryptedText.txt', 'w') as file:
            file.write(plaintext)
        return plaintext

class ECDSA:
    def __init__(self, curve, keypair = None):
        self.curve = curve
        self.keypair = keypair
    def ECDSA_sign(self, privateKey, message):
            # Convert message to bytes
            message_bytes = message.encode()

            # Hash message
            message_hash = hashlib.sha512(message_bytes).hexdigest()
            message_int = int(message_hash, 16)

            # Generate random number k
            k = random.getrandbits(20)

            # Calculate r = x1 mod n
            x1 = self.curve.g.ECmultiply(k).x
            r = x1 % self.curve.field.n

            # Calculate s = k^-1 (z + r * d) mod n
            d = privateKey
            z = message_int
            k_inv = mod_inverse(k, self.curve.field.n)
            s = (k_inv * (z + r * d)) % self.curve.field.n

            return r, s
    def ECDSA_verify(self, publicKey, message, signature):
            r, s = signature

            # Convert message to bytes
            message_bytes = message.encode()

            # Hash message
            message_hash = hashlib.sha512(message_bytes).hexdigest()
            message_int = int(message_hash, 16)

            # Calculate w = s^-1 mod n
            s_inv = mod_inverse(s, self.curve.field.n)

            # Calculate u1 = zw mod n and u2 = rw mod n
            z = message_int
            u1 = (z * s_inv) % self.curve.field.n
            u2 = (r * s_inv) % self.curve.field.n

            # Calculate x1 = u1 * G + u2 * Q
            x1 = self.curve.g.ECmultiply(u1).ECadd_point(publicKey.ECmultiply(u2)).x

            return r == x1 % self.curve.field.n