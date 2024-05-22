from CSPRNG.csprng import CSPRNG
from RSA.rsa import RSA

rsa = RSA()

csprng = CSPRNG(32) # Unused so far, might need generated prime numbers
csprng.rand_int(0, 100)

private_key, public_key = rsa.generate_keypair()
rsa.save_keys_to_files(private_key, public_key)

private_key, public_key = rsa.load_keys_from_files()

msg = 'you should commit sewer side'
msg_byt = msg.encode('utf-8')  # convert to bytes; alternatively add b before str
ciphertext = rsa.encrypt(public_key, msg_byt)
print(f'Ciphertext: {ciphertext}')

dec_msg_byt = rsa.decrypt(private_key, ciphertext)
dec_msg = dec_msg_byt.decode('utf-8')  # convert back
print(f'Decrypted message: {dec_msg}')
