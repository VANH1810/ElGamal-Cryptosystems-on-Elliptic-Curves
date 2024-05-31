import random
import math

def fast_power(a, d, n):
    result = 1
    while d > 0:
        if d % 2 == 1:
            result = (result * a) % n
        a = (a**2) % n
        d //= 2
    return result

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
def LowLevelPrimeCheck(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    for divisor in first_primes_list:
        if n % divisor == 0 and divisor**2 <= n:
            return False
    return True
def Miller_Rabin_Prime_Check(n, k=20):
    def check(a, s, d, n):
        x = fast_power(a, d, n)
        if x == 1:
            return True
        for _ in range(s - 1):
            if x == n - 1:
                return True
            x = fast_power(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        if not check(a, s, d, n):
            return False

    return True

def generate_prime(bits):
    while True:
        p = random.randint(2**(bits-1), 2**bits - 1)
        if p % 2 == 0:
            p += 1
        if LowLevelPrimeCheck(p):
            if Miller_Rabin_Prime_Check(p):
                return p

bit_n = 256
p = generate_prime(bit_n)
print(p)

#937151