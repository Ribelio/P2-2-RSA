import base64
import time
import random
import numpy as np
import os
import sys
import RSA.rsa_CSPRNG

from cryptography.hazmat.primitives import padding, hashes
from check_decryption import WordChecker


class Timing:
    """
    This class is used for decryption attacks on RSA through the use of timing. 
    """

    # Step 1: Read the encrypted message information like public key and exponent
    def read_encryption_txt(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

        encrypted = base64.b64decode(lines[1].strip())
        n = int(lines[4].strip())
        e = int(lines[7].strip())

        return encrypted, n, e

    # Step 2: Get an approximate of the private key (sophisticated techniques not possible)
    def generate_d_approx(self):
        key_size = 2048
        p = rsa_CSPRNG.generate_prime_number(key_size // 2, random)
        q = rsa_CSPRNG.generate_prime_number(key_size // 2, random)

        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537  # commonly used prime exponent
        d = pow(e, -1, phi)  # modular inverse

        return n, e, d

    # Step 3: Decrypt with timing information
    def derive_private_key(self, ciphertext, d, n):
        start_time = time.perf_counter()

        # square-and-multiply method
        m = 1
        for bit in bin(d)[2:]:
            m = (m * m) % n
            if bit == '1':
                m = (m * ciphertext) % n
            # different timing based on bit value
            time.sleep(0.00001 if bit == '1' else 0.000005)

        end_time = time.perf_counter()
        decryption_time = end_time - start_time
        return m, decryption_time

    # Step 4: Decrypt message using private key
    def decrypt_message(self, private_key, ciphertext):
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    # Step 5: Combine all steps
    def timing_decrypt(self, file):
        encrypted, n, e = self.read_encryption_txt(file)
        no1, no2, d = self.generate_d_approx()
        private_key = self.derive_private_key(encrypted, d, n)
        bytes_plaintext = self.decrypt_message(private_key, encrypted)
        plaintext = bytes_plaintext.decode('utf-8')

        tokens = self.word_checker.tokenize(plaintext)
        correct_words = self.word_checker.count_correct_words(tokens)
        ratio = correct_words / len(tokens)
        print("The ratio of english words to total words is: " + str(ratio))
        if ratio < 0.70:
            raise ValueError("The decrypted text does not contain enough English words to be counted to have been decrypted")
        return plaintext

if __name__ == "__main__":
    timing = Timing()
    n, e, d = timing.generate_d_approx()
    print("Generated RSA keys.")
    print("n ", n, "\n", "e ", e, "\n", "d ", d)

    message = 42
    ciphertext = pow(message, e, n)

    inferred_d = 0
    max_rounds = 10

    for round_number in range(max_rounds):
        print(f"Round {round_number + 1}/{max_rounds}")
        # collect timing data
        num_samples = 1000
        timing_data = []

        for _ in range(num_samples):
            _, decryption_time = timing.derive_private_key(ciphertext, d, n)
            timing_data.append(decryption_time)

        print("Timing data collected.")

        # timing analysis to infer bits of d
        timing_data = np.array(timing_data)
        threshold = timing_data.mean()

        inferred_d_bits = []
        for bit_position in range(d.bit_length()):
            print(f"Inferring bit {bit_position + 1}/{d.bit_length()}")
            bit_timings = timing_data[bit_position::d.bit_length()]
            if bit_timings.mean() > threshold:
                inferred_d_bits.append('1')
            else:
                inferred_d_bits.append('0')

        inferred_d = int(''.join(inferred_d_bits), 2)
        print(f"Inferred d: {inferred_d}")
        print(f"Actual d: {d}")
        print(f"Correct: {inferred_d == d}")

        if d == inferred_d:  # this is good as a test, but real world scenarios would make use of word detection
            break
        else:
            print("Incorrect inference, continuing to next round.")
    else:
        print("Failed to correctly infer the private key after maximum rounds.")
