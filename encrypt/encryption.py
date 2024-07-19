import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh, ec, rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives import serialization
from numpy import cos
from Crypto.Cipher import AES
from bb84 import generate_bb84_key

# 生成一个16字节的随机初始向量（IV）
def generate_iv():
    return os.urandom(16)

# 对称加密（AES）
def encrypt_aes(data, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return iv + cipher.encrypt(data)

# 对称解密（AES）
def decrypt_aes(encrypted_data, key):
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(encrypted_data[16:])

# 非对称加密（RSA）
def encrypt_rsa(data, public_key):
    return public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

# 非对称解密（RSA）
def decrypt_rsa(encrypted_data, private_key):
    return private_key.decrypt(encrypted_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

# 混沌加密
class LogisticMapEncryption:
    def __init__(self, seed):
        self.seed = seed

    def encrypt(self, data):
        encrypted_data = []
        x = self.seed
        for byte in data:
            for _ in range(8):
                x = 4.0 * x * (1 - x)
                encrypted_data.append(byte ^ int(256 * x) % 256)
        return bytes(encrypted_data)

    def decrypt(self, encrypted_data):
        return self.encrypt(encrypted_data)  # Decryption is the same as encryption

class ChebyshevMapEncryption:
    def __init__(self, seed):
        self.seed = seed

    def encrypt(self, data):
        encrypted_data = []
        x = self.seed
        for byte in data:
            for _ in range(8):
                x = cos(2 * cos(x))
                encrypted_data.append(byte ^ int(256 * x) % 256)
        return bytes(encrypted_data)

    def decrypt(self, encrypted_data):
        return self.encrypt(encrypted_data)  # Decryption is the same as encryption

# 生成随机 AES 密钥
def generate_aes_key():
    return os.urandom(32)  # 256-bit 密钥

# 生成 RSA 密钥对
def generate_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# 生成用于密钥交换的 Diffie-Hellman 密钥对
def generate_diffie_hellman_keys():
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

# 生成用于密钥交换的 ECDH 密钥对
def generate_ecdh_keys():
    private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# 组合加密方法
def combined_encrypt(data, methods):
    encrypted_data = data
    for method, params in methods:
        encrypted_data = method(encrypted_data, **params)
    return encrypted_data

# 组合解密方法
def combined_decrypt(data, methods):
    decrypted_data = data
    for method, params in reversed(methods):
        decrypted_data = method(decrypted_data, **params)
    return decrypted_data

# 加密文件内容
def encrypt_file_content(file_content, methods):
    return combined_encrypt(file_content, methods)

# 解密文件内容
def decrypt_file_content(file_content, methods):
    return combined_decrypt(file_content, methods)