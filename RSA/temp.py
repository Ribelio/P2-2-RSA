from CSPRNG.csprng import CSPRNG
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from sympy import isprime, nextprime
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_prime_candidate(length, random):
    """ Generate an odd integer randomly """
    p = random.rand_int(2 ** (length - 1), 2 ** length - 1)
    return p | 1  # Ensure the number is odd


def generate_prime_number(length, random):
    """ Generate a prime number of `length` bits """
    p = 4
    # Keep generating while the number is not prime
    while not isprime(p):
        p = generate_prime_candidate(length, random)
    return p


def generate_rsa_keypair(random, key_size=2048):
    p = generate_prime_number(key_size // 2, random)
    q = generate_prime_number(key_size // 2, random)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Commonly used prime exponent
    d = pow(e, -1, phi)  # Modular inverse

    # Create private and public key objects
    privatekey = rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=rsa.rsa_crt_dmp1(d, p),
        dmq1=rsa.rsa_crt_dmq1(d, q),
        iqmp=rsa.rsa_crt_iqmp(p, q),
        public_numbers=rsa.RSAPublicNumbers(e, n)
    ).private_key()

    publickey = privatekey.public_key()
    return privatekey, publickey


# Save keys to files
def save_keys_to_files(privatekey, publickey):
    pem_private_key = privatekey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key_temp.pem', 'wb') as f:
        f.write(pem_private_key)

    pem_public_key = publickey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key_temp.pem', 'wb') as f:
        f.write(pem_public_key)


# Load keys from files
def load_keys_from_files():
    with open('private_key_temp.pem', 'rb') as f:
        privatekey = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    with open('public_key_temp.pem', 'rb') as f:
        publickey = serialization.load_pem_public_key(
            f.read()
        )
    return privatekey, publickey


# Encrypt a message
def encrypt_message(publickey, message1):
    ciphertext1 = publickey.encrypt(
        message1,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext1


# Decrypt a message
def decrypt_message(privatekey, ciphertext1):
    plaintext = privatekey.decrypt(
        ciphertext1,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext
