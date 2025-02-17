from cryptography.fernet import Fernet
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

import os, base64

PRIVATE_KEY_PATH = "private.pem"
PUBLIC_KEY_PATH = "public.pem"

class cipher_suite:
    def __init__(self):
        self.fernet_key = b'k1HTWLUzzY7hPg-TjWTX9uoeHBtCH_i5cW8xQgCiiZw='
        self.aes_key = b',-\xc7|m\xd5j\x05\xfa\x06\x95\xc5\xffY\x15\xb6'
        self.fernet_cipher = Fernet(key=self.fernet_key)
        if not os.path.exists(PRIVATE_KEY_PATH):
            key = RSA.generate(2048)
            with open(PRIVATE_KEY_PATH, "wb") as priv_file:
                priv_file.write(key.export_key())
            with open(PUBLIC_KEY_PATH, "wb") as pub_file:
                pub_file.write(key.publickey().export_key())

        with open(PRIVATE_KEY_PATH, "rb") as priv_file:
            self.private_key = priv_file.read()
        
        with open(PUBLIC_KEY_PATH, "rb") as pub_file:
            self.public_key = pub_file.read()

    #Symmetric encryption
    def fernet_encrypt(self, data):
        return self.fernet_cipher.encrypt(data.encode()).decode()

    def fernet_decrypt(self, encrypted_data):
        return self.fernet_cipher.decrypt(encrypted_data.encode()).decode()

    #AES encryption
    def aes_encrypt(self, data):
        iv = os.urandom(16)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        encrypted_bytes = cipher.encrypt(self.pad(data).encode())
        return base64.b64encode(iv + encrypted_bytes).decode()
    
    def aes_decrypt(self, data):
        data = base64.b64decode(data)
        iv = data[:16]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(data[16:]).decode())

    
    def pad(self, s):
        return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    def unpad(self, s):
        return s[:-ord(s[-1])]
    #RSA encryption
    def rsa_encrypt(self, data):
        rsa_key = RSA.import_key(self.public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted_bytes = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_bytes).decode()

    def rsa_decrypt(self, encrypted_data):
        rsa_key = RSA.import_key(self.private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        decrypted_bytes = cipher.decrypt(base64.b64decode(encrypted_data))
        return decrypted_bytes.decode()

def select_cipher(cipher_suite, cipher_type, data):
    match cipher_type:
        case "symmetric":
            return cipher_suite.fernet_encrypt(data)
        case "aes":
            return cipher_suite.aes_encrypt(data)
        case "rsa":
            return cipher_suite.rsa_encrypt(data)
        
def select_decipher(cipher_suite, cipher_type, data):
    match cipher_type:
        case "symmetric":
            return cipher_suite.fernet_decrypt(data)
        case "aes":
            return cipher_suite.aes_decrypt(data)
        case "rsa":
            return cipher_suite.rsa_decrypt(data)