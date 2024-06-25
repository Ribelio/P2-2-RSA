from sympy import primefactors
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import sympy
from check_decryption import WordChecker
import sys

class Mathematical:
    """
    This class is used for decryption attacks on RSA through the exploitation of the mathematics behind RSA.
    The method attempts to factorize the public key to find its prime numbers and construct the private key. 
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
    
    # Step 2: Factorize public key to find prime numbers p and q 
    def find_prime_factors(self, n):
        factors = primefactors(n)
        if len(factors) == 2:
            p, q = factors
            return p, q
    # mathematically: public key of an RSA can always be factorized into two prime numbers
    # realistically: for very large public keys like 2048-bit, it is computationally infeasible to get p and q

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
    def mathematical_decrypt(self, file):
        encrypted, n, e = self.read_encryption_txt(file)
        p, q = self.find_prime_factors(n)
        private_key = self.derive_private_key(p, q, e)
        bytes_plaintext = self.decrypt_message(private_key, encrypted)
        plaintext = bytes_plaintext.decode('utf-8')

        tokens = self.word_checker.tokenize(plaintext)
        correct_words = self.word_checker.count_correct_words(tokens)
        ratio = correct_words / len(tokens)
        print("The ratio of english words to total words is: " + str(ratio))
        if ratio < 0.70:
            sys.exit(3)
        return plaintext

##################################################################################################

if __name__ == "__main__":
    math = Mathematical()
    decrypted_text = math.mathematical_decrypt('encrypted_text_info.txt')
    print(decrypted_text)
    with open('output.txt', 'w') as file:
        file.write(decrypted_text)