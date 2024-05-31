import math
import ECC_Class

# Standard curve database
#secp384r1
#384-bit prime field Weierstrass curve.
#Also known as: P-384ansip384r1

Pcurve = 2**384 - 2**128 - 2**96 + 2**32 - 1
a = int('0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000fffffffc', 16)
b = int('0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef' , 16)
Gx = int('0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7' , 16)
Gy = int('0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f' , 16)
n = int('0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973' , 16)
h = 1

print(f"Pcurve = {Pcurve}")
print(f"a = {a}")
print(f"b = {b}")
print(f"Gx = {Gx}")
print(f"Gy = {Gy}")
print(f"n = {n}")
print(f"h = {h}")

private_key = 95417821490057205389247456523822114056799694061108991750322661385198336080023
# Elliptic curve equation: y^2 = x^3 + ax + b
field = ECC_Class.SubGroup(Pcurve, (Gx, Gy), n, h)
curve = ECC_Class.Elliptic_Curves(a, b, field, "secp384r1")
GenPoint = ECC_Class.Point(curve, Gx, Gy)

PubPoint = GenPoint.ECmultiply(private_key)
print(PubPoint)