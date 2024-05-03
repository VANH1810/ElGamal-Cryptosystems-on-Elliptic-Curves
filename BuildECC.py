import random

Z = 937151

def sieve(upper):
	result = []
	prime = [True for i in range(upper)]
	p = 2
	while p<<2 <= upper:
		if prime[p]:
			for i in range(2*p, upper, p):
				prime[i] = False
		p+=1
	for p in range(upper-1, 0,-1):
		if prime[p]:
			result.append(p)
	return result[::-1][1:]

mapping  = {}
for i in range(Z):
    temp = (i*i)%Z
    mapping[temp] = mapping.get(temp, []) + [i]

primes = (sieve(2**20 + 1))
found = {}

print("Start")
while True:
    
    #a,b = random.randrange(1,Z), random.randrange(1,Z)
    a,b = 872338, 842444
    print(f"Trying a = {a}, b = {b}")
    
    if (4*a**3 + 27*b**2) % Z == 0:
        continue
    cnt = 1
    for x in range(0,Z):
        y = (x*x*x + a*x + b) % Z
        if (y) in mapping:
            #print(x, mapping[y])
            found[(x,y)] = mapping[y]
            cnt += len(mapping[y])
        else:
            pass
    
    if (cnt in primes):
        print("[Order of G]: ", cnt)
        break
        
print(f"Found a = {a}, b = {b}")

#[Order of G] 937537