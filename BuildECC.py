import random
from collections import defaultdict

Z = 937151 # Pcurve

# Sieve of Eratosthenes
def sieve(upper):
    if upper < 2:
        return []  # Return an empty list if there are no primes in the range

    prime = [True] * upper  # Initialize the prime list
    prime[0] = prime[1] = False  # 0 and 1 are not prime numbers
    result = []

    for p in range(2, int(upper**0.5) + 1):
        if prime[p]:
            for i in range(p*p, upper, p):
                prime[i] = False

    for p in range(2, upper):
        if prime[p]:
            result.append(p)

    return result

mapping = defaultdict(list)
for i in range(Z):
    temp = (i*i) % Z
    mapping[temp].append(i)

# Assuming sieve function is defined elsewhere
primes = sieve(2**20 + 1)
found = {}

print("Start")
while True:
    
    a,b = random.randrange(1,Z), random.randrange(1,Z)
    #a,b = 872338, 842444 # Acurve, Bcurve
    print(f"Trying a = {a}, b = {b}")
    
    if (4*a**3 + 27*b**2) % Z == 0:
        continue
    cnt = 1
    for x in range(0,Z):
        y = (x*x*x + a*x + b) % Z
        if (y) in mapping:
            #print(x, mapping[y]) # Point in the curve
            found[(x,y)] = mapping[y]
            cnt += len(mapping[y])
        else:
            pass
    
    if (cnt in primes):
        print("[Order of G]: ", cnt)
        break
        
print(f"Found a = {a}, b = {b}")

#[Order of G] 937537