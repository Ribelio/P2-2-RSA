# CSPRNG Flask API

Instruction for our API documentation, this Flask API provides cryptographically secure pseudorandom number generation (CSPRNG) through a simple HTTP interface. The API generates random numbers using OS-specific CSPRNG mechanisms and can be easily extended or integrated into various applications. The project can also be run in Java with either `RSA\GUI.java` or `CSPRNG\RNGUI.java`.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- (Optional) Docker if you prefer containerization

### Steps

1. **Clone the repository**:

    ```bash
    git clone REPO
    cd csprng-flask-api
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the API

To start the Flask API, simply run:

```bash
python CSPRNG\\API_connection.py.py
```

# MAIN GUI Usage (RSA Encryption and Decryption)

To get started, run the GUI.java file found under the RSA folder.

## Encryption

To encrypt, simply type in a message into the input box and click ENCRYPT. Then the resulting encoded message will appear in the output box. 

## Decryption

To decrypt, enter an encrypted message along with the public key and public exponent. Then choose one of the attack methods available using the radio buttons. Once done,
click DECRYPT to receive the output. 

## Testing the decryption 

To confirm that a message is being correctly decrypted you can do the following:
1. Go to the decrypt_rsa.py class found under the 'Decrypt' folder.
2. Find message="text" at line (145) and replace it with any message.
3. Run decrypt_rsa.py. This will overwrite the encrypted message, public key, and public exponent into the file "encrypted_text_info.txt" (found in the main project folder)
4. Copy and paste this data into the decryption tab in the UI, choose "mathematical attack" and decrypt.

Attempting to use the Bruteforce method will inform you that the public key is too long to attempt bruteforce decryption. Instead, the bruteforce can be tested as follows: 
1. Navigate to Decrypt/decrypt_rsa.py
2. Comment lines 91 - 113 (encrpyt/decrypt a message - good padding)
3. Uncomment lines 115 - 129 (encrpyt/decrypt a message - worse padding)
4. Change the key size at line 36 from 2048 to 500
5. This will ensure that the encrypted message is much more likely to be decrypted in a feasible amount of time using the bruteforce algorithm
6. Now you can go through the same steps as before (i.e. change the message at line 145, copy the information from the text file...)

NOTE: Please use a SHORT message to encrypt if you want to test the bruteforce decryption (even with the worse padding method, the key size of 500 can only carry enough info for a few words/characters of message length)

NOTE: For the bruteforce, depending on what the limit is set to, the GUI might freeze for some time. E.g. if the limit is 100,000 the bruteforce will take a long time to search for the primes p and q. You can change this limit from Decrypt/bruteforce.py at line 27 for testing purposes.

NOTE: Encrypting a message through the UI's Encrypt tab DOES NOT overwrite "encrypted_text_info.txt". This means that the Encrypt tab does not provide public key and public exponent values. 
