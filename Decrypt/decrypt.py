from mathematical import Mathematical
from bruteforce import Bruteforce

class Decrypt:

    def __init__(self, method, file) -> None:
        self.method = method
        self.file = file
        self.math = Mathematical()
        self.brtf = Bruteforce()
    
    def decrypt(self):
        if self.method == 'mathematical':
            decrypted_text = self.math.mathematical_decrypt(self.file)
            return decrypted_text.decode('utf-8')
        elif self.method == 'bruteforce':
            decrypted_text = self.brtf.bruteforce_decrypt(self.file)
            return decrypted_text.decode('utf-8')
        
decrypter = Decrypt(method = 'bruteforce', file = 'encrypted_text_info.txt')
print(decrypter.decrypt())