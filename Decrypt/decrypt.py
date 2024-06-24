from mathematical import Mathematical
from bruteforce import Bruteforce
from timing import Timing

class Decrypt:

    def __init__(self, method, file = 'encrypted_text_info.txt') -> None:
        self.method = method
        self.file = file
        self.math = Mathematical()
        self.brtf = Bruteforce()
        self.tmng = Timing()
    
    def decrypt(self):
        if self.method == 'mathematical':
            decrypted_text = self.math.mathematical_decrypt(self.file)
            return decrypted_text
        elif self.method == 'bruteforce':
            decrypted_text = self.brtf.bruteforce_decrypt(self.file)
            return decrypted_text.decode('utf-8')
        elif self.method == 'timing':
            decrypted_text = self.tmng.timing_decrypt(self.file)
            return decrypted_text.decode('utf-8')
        
decrypter = Decrypt(method = 'bruteforce')
print(decrypter.decrypt())