import ECC_Class
import random
import math
#The proven prime
Pcurve = 937151

#Elliptic curve: y^2 = x^3 + Acurve * x + Bcurve
Acurve = 872338; Bcurve = 842444

#Generator Point
Gx = 16213 
Gy = 331227
GPoint = (Gx, Gy)

#Number of points in the field [Order of G]
N = 937537

bits = 20
privKey = 562997

#size of each block
block_size = 2

#Initialize the ECC
field = ECC_Class.SubGroup(Pcurve, GPoint, N, 1)
curve = ECC_Class.Elliptic_Curves(Acurve, Bcurve, field, "Vanh_Curve")
KeyPair = ECC_Class.KeyPair(curve, privKey)
CrytoGraphy = ECC_Class.ECC(curve, KeyPair)

#Encryption
message = input("Enter the message: ")
key = input("Enter the key: ")
cipher = CrytoGraphy.encrypt(int(key), message)
#print("Cipher: ", cipher)

#Decryption
plain = CrytoGraphy.decrypt(cipher)
print("Plain: ", plain)

