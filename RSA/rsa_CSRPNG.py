import base64
from csprng import CSPRNG

try:
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization, hashes
    from sympy import isprime, nextprime
    from cryptography.hazmat.primitives.asymmetric import rsa
except ImportError as e:
    print("Error importing required modules:", e)
    print("Please make sure to install the necessary packages.")
    print("You can install the required packages by running the following command:")
    print("pip install cryptography sympy")

    # You can uncomment the following lines to automatically install the packages
    import subprocess
    subprocess.call(['pip', 'install', 'cryptography', 'sympy'])
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization, hashes
    from sympy import isprime, nextprime
    from cryptography.hazmat.primitives.asymmetric import rsa


def generate_prime_candidate(length, random):
    p = random.rand_int(2 ** (length - 1), 2 ** length - 1) # odd int
    return p | 1  # ensure int is odd


def generate_prime_number(length, random): # generate a prime number of `length` bits
    p = 4
    while not isprime(p):  # keep generating while the number is not prime
        p = generate_prime_candidate(length, random)
    return p


def generate_rsa_keypair(random, key_size=2048):
    p = 21 #generate_prime_number(key_size // 2, random)
    q = 17 #generate_prime_number(key_size // 2, random)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # commonly used prime exponent
    d = pow(e, -1, phi)  # modular inverse

    # create private and public key objects
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


# save keys to files
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


# load keys from files
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


# encrypt a message
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


# decrypt a message
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

# save rsa information in a text file
def save_encryption_info(ciphertext, publickey):
    public_nums = publickey.public_numbers()
    n = public_nums.n
    e = public_nums.e

    # shamelessly admitting i formatted this part using chatgpt 
    with open('encrypted_text_info.txt', 'w') as f:
        f.write(f"Encrypted Text (Base64):\n{base64.b64encode(ciphertext).decode('utf-8')}\n\n")
        f.write(f"Public Key (n):\n{n}\n\n")
        f.write(f"Public Exponent (e):\n{e}\n\n")
        f.write(f"Public Key PEM:\n{publickey.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')}\n")

