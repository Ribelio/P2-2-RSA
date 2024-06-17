import itertools
from sympy import primefactors
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import sympy

class Bruteforce:
    """
    This class is used for decryption attacks on RSA through bruteforcing.
    The method attempts to find the prime numbers that make up the public key by going through every prime number. 
    """

    # Step 1: Read the encrypted message information like public key and exponent
    def read_encryption_txt(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

        encrypted = base64.b64decode(lines[1].strip())
        n = int(lines[4].strip())
        e = int(lines[7].strip())

        return encrypted, n, e
    
    # Step 2: Bruteforece attempt to find prime numbers p and q 
    def bruteforce_prime_factors(self, n, limit=1000000):
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

brtf = Bruteforce()
decrypted_text = brtf.bruteforce_decrypt('encrypted_text_info.txt')
print(decrypted_text.decode('utf-8'))