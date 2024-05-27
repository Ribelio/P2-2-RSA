from CSPRNG.csprng import CSPRNG
from RSA import temp
from pathlib import Path


def temptest(message):
    if __name__ == "__main__":
        csprng = CSPRNG(32)  # initialize custom CSPRNG

        # generate RSA keys
        if not (Path.cwd() / 'private_key_temp.pem').exists() or not (Path.cwd() / 'public_key_temp.pem').exists():
            privatekey, publickey = temp.generate_rsa_keypair(csprng)
            temp.save_keys_to_files(privatekey, publickey)
        else:
            # load keys: this step is just to demonstrate loading. in real usage, keys should already be loaded
            privatekey, publickey = temp.load_keys_from_files()

        # encrypt and decrypt a message
        message1 = message.encode('utf-8')
        ciphertext1 = temp.encrypt_message(publickey, message1)
        print(f'Ciphertext: {ciphertext1}')

        decrypted_message1 = temp.decrypt_message(privatekey, ciphertext1)
        print(f'Decrypted message: {decrypted_message1}')

        return decrypted_message1
    return None
