import bruteforce as Bruteforce 

class Decrypt:
    def __init__(self, method, file) -> None:
        self.method = method
        self.file = file
    
    def decrypt(self):
        if self.method == 'bruteforce':
            brtf = Bruteforce()
            decrypted_text = brtf.brute_force_decrypt(self.file)
            return decrypted_text.decode('utf-8')

decrypter = Decrypt(method = 'bruteforce', file = 'encrypted_text_info.txt')
print(decrypter.decrypt())