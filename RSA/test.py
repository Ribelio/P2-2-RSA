from CSPRNG.csprng import CSPRNG
from RSA import rsa
from pathlib import Path  # good for file checking shenanigans


csprng = CSPRNG(32)  # Unused so far, might need generated prime numbers
csprng.rand_int(0, 100)

# print((Path.cwd() / 'private_key.pem').exists(), (Path.cwd() / 'public_key.pem').exists())
# check if keys have already been created
if not (Path.cwd() / 'private_key.pem').exists() or not (Path.cwd() / 'public_key.pem').exists():
    private_key, public_key = rsa.generate_keypair()
    rsa.save(private_key, public_key)
else:
    private_key, public_key = rsa.load()

msg = 'you should commit sewer side'
msg_byt = msg.encode('utf-8')  # convert to bytes; alternatively add b before str
enc_msg = rsa.encrypt(public_key, msg_byt)
print(f'Encrypted message: {enc_msg}')

dec_msg_byt = rsa.decrypt(private_key, enc_msg)
dec_msg = dec_msg_byt.decode('utf-8')  # convert back
print(f'Decrypted message: {dec_msg}')
