from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


# does not yet use csprng
def generate_keypair():
    """
    Generates random public and private keys
    Returns: both keys
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key


# saving and loading not fully necessary yet, but is useful in irl scenarios and can prevent long key generation times
def save(private_key, public_key):
    """
    Saves private and public keys to file
    Args:
        private_key: key for decryption
        public_key: key for encryption
    """
    pem_private = private_key.private_bytes(  # key as bytes
        encoding=serialization.Encoding.PEM,  # output format pem
        format=serialization.PrivateFormat.TraditionalOpenSSL,  # TraditionalOpenSSL is common practice for private keys
        encryption_algorithm=serialization.NoEncryption()  # no password requirement as devs
    )
    with open('private_key.pem', 'wb') as file:  # wb = write-binary
        file.write(pem_private)  # writes file and closes it

    pem_public = public_key.public_bytes(  # same shtick as above
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key.pem', 'wb') as file:
        file.write(pem_public)


# .pem files are used as a standard cryptography format for saving keys (privacy-enhanced mail)
def load():
    """
    Loads private and public keys from file if available
    """
    with open('private_key.pem', 'rb') as file:
        private_key = serialization.load_pem_private_key(  # given function from serialization, no password
            file.read(),
            password=None
        )
    with open('public_key.pem', 'rb') as file:
        public_key = serialization.load_pem_public_key(
            file.read()
        )
    return private_key, public_key


def encrypt(public_key, msg):
    """
    Saves private and public keys to file
    Args:
        public_key: key for encryption
        msg: plaintext message converted to bytes
    Return: encrypted message
    """
    enc_msg = public_key.encrypt(  # start the encryption with public key (pub key would be the csprng affected element)
        msg,
        padding.OAEP(  # standard padding scheme for RSA (adding nonsense), can be subject to research and change
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # standard mask and hash (randomness injection, variable len.)
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return enc_msg


def decrypt(private_key, enc_msg):
    """
    Saves private and public keys to file
    Args:
        private_key: key for decryption
        enc_msg: encrypted message
    Return: decrypted message in byte format
    """
    dec_msg = private_key.decrypt(  # same shtick
        enc_msg,
        padding.OAEP(  # matches encryption
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return dec_msg
