import Decrypt.mathematical as Mathematical 

class Decrypt:
    def __init__(self, method, file) -> None:
        self.method = method
        self.file = file
    
    def decrypt(self):
        if self.method == 'mathematical':
            math = Mathematical()
            decrypted_text = math.brute_force_decrypt(self.file)
            return decrypted_text.decode('utf-8')

decrypter = Decrypt(method = 'mathematical', file = 'encrypted_text_info.txt')
print(decrypter.decrypt())