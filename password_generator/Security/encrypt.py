from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class encryption:

    def __init__(self, userkey):

        self.userkey = userkey
        self.obj = self.get_key(self.userkey)
        

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
        f = Fernet(key)
        return f

    def encode(self, message):
        encrypted = self.obj.encrypt(message.encode())
        return encrypted

    def decode(self, encrypt):
        decrypted = self.obj.decrypt(encrypt)
        return decrypted


