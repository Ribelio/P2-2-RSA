import itertools
from sympy import primefactors
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import sympy
import sys
from check_decryption import WordChecker 
import math

class Bruteforce:
    """
    This class is used for decryption attacks on RSA through bruteforcing.
    The method attempts to find the prime numbers that make up the public key by going through every prime number.
    """
    
    def __init__(self) -> None:
        self.word_checker = WordChecker()

    # Step 1: Read the encrypted message information like public key and exponent
    def read_encryption_txt(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

        encrypted = base64.b64decode(lines[1].strip())
        n = int(lines[4].strip())
        e = int(lines[7].strip())

        return encrypted, n, e

    # Step 2: Bruteforece attempt to find prime numbers p and q 
    def bruteforce_prime_factors(self, n, limit=100):
        primes = list(sympy.primerange(2, limit))
        temp = primes
        for prime in primes:
            if prime > math.sqrt(n):
                temp.pop()
        primes = temp
        for p, q in itertools.combinations(primes, 2):
            if p * q == n:
                return p, q
        # Return None if the primes are not found within the limit
        return None, None

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
        if p is None or q is None:
            raise ValueError("Limit too small to find p and q")
        private_key = self.derive_private_key(p, q, e)
        bytes_plaintext = self.decrypt_message(private_key, encrypted)
        plaintext = bytes_plaintext.decode('utf-8')
        
        tokens = self.word_checker.tokenize(plaintext)
        correct_words = self.word_checker.count_correct_words(tokens)
        ratio = correct_words / len(tokens)
        print("The ratio of english words to total words is: " + str(ratio))
        return plaintext, ratio

##################################################################################################

if __name__ == "__main__":
    brtf = Bruteforce()
    try:
        decrypted_text, ratio = brtf.bruteforce_decrypt('encrypted_text_info.txt')
        print(decrypted_text)
        with open('output.txt', 'w') as file:
            file.write(decrypted_text)
        if ratio < 0.70:
            sys.exit(3)
    except ValueError as ve:
        if str(ve) == "Limit too small to find p and q":
            print("Specific error: Limit too small to find p and q", file=sys.stderr)
            sys.exit(2)  
        else:
            print(f"ValueError: {ve}", file=sys.stderr)
            sys.exit(1)  
    except Exception as e:
        print(f"General error: {e}", file=sys.stderr)
        sys.exit(1) 