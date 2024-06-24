from csprng import CSPRNG
import RSA.rsa_CSPRNG as rsa_CSPRNG
from pathlib import Path

def encrypt_CSPRNG(message):
    csprng = csprng.CSPRNG(32)  # initialize custom CSPRNG

    # generate RSA keys
    #if not (Path.cwd() / 'private_key_temp.pem').exists() or not (Path.cwd() / 'public_key_temp.pem').exists():
    privatekey, publickey = rsa_CSPRNG.generate_rsa_keypair(csprng)
    rsa_CSPRNG.save_keys_to_files(privatekey, publickey)
    # else:
    #     # load keys: this step is just to demonstrate loading. in real usage, keys should already be loaded
    #     privatekey, publickey = rsa_CSRPNG.load_keys_from_files()

    # encrypt and decrypt a message
    message1 = message.encode('utf-8')
    ciphertext1 = rsa_CSPRNG.encrypt_message(publickey, message1)
    print(f'Ciphertext: {ciphertext1}')

    decrypted_message1 = rsa_CSPRNG.decrypt_message(privatekey, ciphertext1)
    print(f'Decrypted message: {decrypted_message1}')

    # Write the output to a file
    #with open('output.bin', 'wb') as f:
    #    f.write(ciphertext1)

with open('input.txt', 'r') as file:
    message = file.read().strip()
    csprng = CSPRNG(32)  # initialize custom CSPRNG

    # generate RSA keys
    if not (Path.cwd() / 'private_key_temp.pem').exists() or not (Path.cwd() / 'public_key_temp.pem').exists():
        privatekey, publickey = rsa_CSPRNG.generate_rsa_keypair(csprng)
        rsa_CSPRNG.save_keys_to_files(privatekey, publickey)
    else:
        # load keys: this step is just to demonstrate loading. in real usage, keys should already be loaded
        privatekey, publickey = rsa_CSPRNG.load_keys_from_files()

    # encrypt and decrypt a message
    message1 = message.encode('utf-8')
    ciphertext1 = rsa_CSPRNG.encrypt_message(publickey, message1)
    print(f'Ciphertext: {ciphertext1}')

    decrypted_message1 = rsa_CSPRNG.decrypt_message(privatekey, ciphertext1)
    print(f'Decrypted message: {decrypted_message1}')
    
    #Write the output to a file
    with open('output.bin', 'wb') as f:
        f.write(ciphertext1)
