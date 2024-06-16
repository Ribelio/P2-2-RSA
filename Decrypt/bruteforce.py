from sympy import primefactors
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import sympy
import math

class Bruteforce:

    # Step 1: Read the encrypted message information like public key and exponent
    def read_encryption_txt(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

        encrypted = lines[1].strip()
        n = int(lines[4].strip())
        e = int(lines[7].strip())

        return encrypted, n, e
    
    # Step 2: Factorize public key to find prime numbers p and q 
    def find_prime_factors(self, n):
        factors = primefactors(n)
        if len(factors) == 2:
            p, q = factors
            return p, q
    # mathematically: public key of an RSA can always be factorized into two prime numbers
    # realistically: for very large public keys like 2048-bit, it is computationally infeasible to get p and q

    # Step 3: Derive the private key using p, q, and e
    def derive_private_key(self, p, q, e):
        phi = (p - 1)*(q - 1)
        d = pow(e, -1, phi)
        return rsa.RSAPrivateNumbers(
            p=p,
            q=q,
            d=d,
            dmp1=rsa.rsa_crt_dmp1(d, p),
            dmq1=rsa.rsa_crt_dmq1(d, q),
            iqmp=rsa.rsa_crt_iqmp(p, q),
            public_numbers=rsa.RSAPublicNumbers(e=e, n=p*q)
        ).private_key()
    # see (https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation) for details and report writing

    # Step 4: Decrypt message using private key
    # TODO

##################################################################################################

brtf = Bruteforce()
a,b,c = brtf.read_encryption_txt('encrypted_text_info.txt')
print(f"message = {a} and n = {b} and e = {c}")

n = 8079251517827751825178719172167487990111025667428871008032586356881163784716972723299300352880728365922179490230474504873529889787622730273772038096612070780157719341825249022937549437597413026699014409596016892069198054660654939049996794857126633704285256415786316072175545289935442209782004368095424124754509240475862840949909159226754727392544216087434490676832368797204934292220926874434534118448098885909800474506478094372637703074502097801729719633703577708353501306952896395854091754582002553680744721089534247602346252579494571078057764602026967469991659905115934722261034269954271777343604725328949406257127
p, q = brtf.find_prime_factors(n)
print(f"p = {p} and q = {q}")