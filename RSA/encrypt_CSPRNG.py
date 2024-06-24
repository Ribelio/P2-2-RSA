import base64
from csprng import CSPRNG
import rsa_CSRPNG
from pathlib import Path

def encrypt_CSPRNG(message):
    csprng = csprng.CSPRNG(32)  # initialize custom CSPRNG

    # generate RSA keys
    #if not (Path.cwd() / 'private_key_temp.pem').exists() or not (Path.cwd() / 'public_key_temp.pem').exists():
    privatekey, publickey = rsa_CSRPNG.generate_rsa_keypair(csprng)
    rsa_CSRPNG.save_keys_to_files(privatekey, publickey)
    # else:
    #     # load keys: this step is just to demonstrate loading. in real usage, keys should already be loaded
    #     privatekey, publickey = rsa_CSRPNG.load_keys_from_files()

    # encrypt and decrypt a message
    message1 = message.encode('utf-8')
    ciphertext1 = rsa_CSRPNG.encrypt_message(publickey, message1)
    print(f'Ciphertext: {ciphertext1}')

    decrypted_message1 = rsa_CSRPNG.decrypt_message(privatekey, ciphertext1)
    print(f'Decrypted message: {decrypted_message1}')

    # Write the output to a file
    #with open('output.bin', 'wb') as f:
    #    f.write(ciphertext1)

with open('input.txt', 'r') as file:
    message = file.read().strip()
    csprng = CSPRNG(32)  # initialize custom CSPRNG

    # generate RSA keys
    if not (Path.cwd() / 'private_key_temp.pem').exists() or not (Path.cwd() / 'public_key_temp.pem').exists():
        privatekey, publickey = rsa_CSRPNG.generate_rsa_keypair(csprng)
        rsa_CSRPNG.save_keys_to_files(privatekey, publickey)
    else:
        # load keys: this step is just to demonstrate loading. in real usage, keys should already be loaded
        privatekey, publickey = rsa_CSRPNG.load_keys_from_files()

    # encrypt and decrypt a message
    message1 = message.encode('utf-8')
    ciphertext1 = rsa_CSRPNG.encrypt_message(publickey, message1)
    print(f'Ciphertext: {ciphertext1}')

    ciphertext_base64 = base64.b64encode(ciphertext1).decode('utf-8')

    decrypted_message1 = rsa_CSRPNG.decrypt_message(privatekey, ciphertext1)
    print(f'Decrypted message: {decrypted_message1}')
    
    #Write the output to a file
    with open('output.txt', 'w') as f:
        f.write(f"{ciphertext_base64}")

    numbers = publickey.public_numbers()
    n = numbers.n
    e = numbers.e

    with open('encrypted_text_info.txt', 'w') as file:
        file.write(f"Encrypted Text (Base64):\n{ciphertext_base64}\n\n")
        file.write(f"Public Key (n):\n{n}\n\n")
        file.write(f"Public Exponent (e):\n{e}\n\n")