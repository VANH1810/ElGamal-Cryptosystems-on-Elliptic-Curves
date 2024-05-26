import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ECC_Class
import random
import math

public_key_values = {}
# Open the file in read mode
with open('ECC - Encrypt and Decrypt/publicKey.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(': ')
        public_key_values[key] = int(value)
print(public_key_values)

#Initialize the ECC
Pcurve = public_key_values['Pcurve']
Acurve = public_key_values['Acurve']
Bcurve = public_key_values['Bcurve']
GPoint = (public_key_values['Gx'], public_key_values['Gy'])
N = public_key_values['OrderG']

field = ECC_Class.SubGroup(Pcurve, GPoint, N, 1)
curve = ECC_Class.Elliptic_Curves(Acurve, Bcurve, field, "Vanh_Curve")
publicPoint = ECC_Class.Point(curve, public_key_values['PublicKeyPoint.x'], public_key_values['PublicKeyPoint.y'])
bits = public_key_values['bits']
block_size = public_key_values['block_size']

Signature_Scheme = ECC_Class.ECDSA(curve, None)

# Open the file in read mode
signature_value = {}
with open('ECDSA/message.txt', 'r') as file:
    message = file.read().strip()
with open('ECDSA/signature.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(': ')
        signature_value[key] = int(value)
signature = (signature_value['r'], signature_value['s'])

# Verify the signature
if Signature_Scheme.ECDSA_verify(publicPoint, message, signature):
    print("Signature is valid")
else:
    print("Signature is invalid")