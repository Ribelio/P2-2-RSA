import itertools
from sympy import primefactors
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import sympy

class Bruteforce:

    # Step 1: Read the encrypted message information like public key and exponent
    def read_encryption_txt(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

        encrypted = base64.b64decode(lines[1].strip())
        n = int(lines[4].strip())
        e = int(lines[7].strip())

        return encrypted, n, e
    
    # Step 2: Bruteforece attempt to find prime numbers p and q 
    def bruteforce_prime_factors(self, n, limit=10000):
            primes = list(sympy.primerange(2, limit))
            for p, q in itertools.combinations(primes, 2):
                if p * q == n:
                    return p, q
                else:
                    raise ValueError("Limit too small to find p and q")

    # Step 3: Derive the private key using p, q, and e (same process as in RSA class)
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

    # Step 4: Decrypt message using private key (same process as in RSA class)
    def decrypt_message(self, privatekey, ciphertext):
        plaintext = privatekey.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    # Step 5: Combine all steps
    def bruteforce_decrypt(self, file):
        encrypted, n, e = self.read_encryption_txt(file)
        p, q = self.bruteforce_prime_factors(n)
        private_key = self.derive_private_key(p, q, e)
        return self.decrypt_message(private_key, encrypted)

##################################################################################################

# math = Mathematical()
# a,b,c = math.read_encryption_txt('encrypted_text_info.txt')
# print(f"message = {a} and n = {b} and e = {c}")

# n = 8079251517827751825178719172167487990111025667428871008032586356881163784716972723299300352880728365922179490230474504873529889787622730273772038096612070780157719341825249022937549437597413026699014409596016892069198054660654939049996794857126633704285256415786316072175545289935442209782004368095424124754509240475862840949909159226754727392544216087434490676832368797204934292220926874434534118448098885909800474506478094372637703074502097801729719633703577708353501306952896395854091754582002553680744721089534247602346252579494571078057764602026967469991659905115934722261034269954271777343604725328949406257127
# p, q = math.find_prime_factors(n)
# print(f"p = {p} and q = {q}")

brtf = Bruteforce()
decrypted_text = brtf.bruteforce_decrypt('encrypted_text_info.txt')
print(decrypted_text.decode('utf-8'))