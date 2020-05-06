from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class encryption:

    def __init__(self, userkey, message):

        self.userkey = userkey
        self.message = message.encode()
        self.key = self.get_key(self.userkey)
        self.obj, self.encrypted = self.encode(self.key, self.message)
        self.decrypted = ''


    def get_key(self, key):
        password = key.encode() # Convert to type bytes
        salt = b'salt_'
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

        return key

    def encode(self, key, message):
        f = Fernet(key)
        encrypted = f.encrypt(message)
        return f, encrypted

    def decode(self, f, encrypt):

        decrypted = f.decrypt(self.encrypted)
        return decrypted
"""
#Driver Code
#Provided by User
message = ""
key = ""
e = encryption(key, message)
print("Encrypted: ", e.encrypted.decode())
print("Decrypted: ",e.decode(e.obj, e.encrypted).decode())
"""
