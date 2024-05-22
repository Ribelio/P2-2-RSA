from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


# saving and loading not fully necessary yet, but is useful in irl scenarios and can prevent long key generation times
def save(private_key, public_key):
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key.pem', 'wb') as f:
        f.write(pem_private_key)

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key.pem', 'wb') as f:
        f.write(pem_public_key)


def generate_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def load():
    with open('private_key.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    with open('public_key.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read()
        )
    return private_key, public_key


def encrypt(public_key, msg):
    ciphertext = public_key.encrypt(
        msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt(private_key, enc_msg):
    dec_msg = private_key.decrypt(
        enc_msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return dec_msg
