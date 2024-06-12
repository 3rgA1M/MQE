from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh, dsa, ec
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives import hashes
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import Aer
import random
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

# 生成一个16字节的随机初始向量（IV）
iv = os.urandom(16)
print("IV 是:", iv)

# 生成用于密钥交换的 Diffie-Hellman 密钥对
def generate_diffie_hellman_keys():
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key


# 生成用于密钥交换的 ElGamal 密钥对
def generate_elgamal_keys():
    private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# Diffie-Hellman 密钥交换
diffie_hellman_private_key, diffie_hellman_public_key = generate_diffie_hellman_keys()

# ElGamal 密钥交换
elgamal_private_key, elgamal_public_key = generate_elgamal_keys()

# 使用 Diffie-Hellman 公钥加密数据
def encrypt_diffie_hellman(data, public_key):
    shared_key = diffie_hellman_private_key.exchange(public_key)
    return encrypt(data, shared_key)

# 使用 ElGamal 公钥加密数据
def encrypt_elgamal(data, public_key):
    ciphertext = public_key.encrypt(data, ec.ECIES())
    return ciphertext

# 使用 Diffie-Hellman 私钥解密数据
def decrypt_diffie_hellman(encrypted_data):
    shared_key = diffie_hellman_private_key.exchange(elgamal_public_key)
    return decrypt(encrypted_data, shared_key)

# 使用 ElGamal 私钥解密数据
def decrypt_elgamal(encrypted_data):
    plaintext = elgamal_private_key.decrypt(encrypted_data, ec.ECIES())
    return plaintext

# 读取待加密的文本文件
with open("input.txt", "rb") as file:
    plaintext = file.read()

# 使用 Diffie-Hellman 公钥加密数据
encrypted_data_diffie_hellman = encrypt_diffie_hellman(plaintext, diffie_hellman_public_key)

# 使用 ElGamal 公钥加密数据
encrypted_data_elgamal = encrypt_elgamal(plaintext, diffie_hellman_public_key)

# 保存加密后的数据到文件
with open("encrypted_diffie_hellman.txt", "wb") as file:
    file.write(encrypted_data_diffie_hellman)

with open("encrypted_elgamal.txt", "wb") as file:
    file.write(encrypted_data_elgamal)

# 使用 Diffie-Hellman 私钥解密数据
decrypted_data_diffie_hellman = decrypt_diffie_hellman(encrypted_data_diffie_hellman)

# 使用 ElGamal 私钥解密数据
decrypted_data_elgamal = decrypt_elgamal(encrypted_data_elgamal)

# 保存解密后的数据到文件
with open("decrypted_diffie_hellman.txt", "wb") as file:
    file.write(decrypted_data_diffie_hellman)

with open("decrypted_elgamal.txt", "wb") as file:
    file.write(decrypted_data_elgamal)

# 打印解密后的数据
print("Diffie-Hellman 解密后的数据:")
print(decrypted_data_diffie_hellman)
print("ElGamal 解密后的数据:")
print(decrypted_data_elgamal)

# MD5 和 RIPEMD-160 哈希函数
def hash_md5(data):
    digest = hashes.Hash(hashes.MD5(), backend=default_backend())
    digest.update(data)
    return digest.finalize()

def hash_ripemd160(data):
    digest = hashes.Hash(hashes.RIPEMD160(), backend=default_backend())
    digest.update(data)
    return digest.finalize()

# 读取待哈希的文本文件
with open("hash_input.txt", "rb") as file:
    plaintext = file.read()

# 对明文数据进行 MD5 哈希
md5_hashed_data = hash_md5(plaintext)

# 对明文数据进行 RIPEMD-160 哈希
ripemd160_hashed_data = hash_ripemd160(plaintext)

# 保存哈希值到文件
with open("md5_hashed.txt", "wb") as file:
    file.write(md5_hashed_data)

with open("ripemd160_hashed.txt", "wb") as file:
    file.write(ripemd160_hashed_data)

# 打印哈希值
print("MD5 哈希值:")
print(md5_hashed_data)
print("RIPEMD-160 哈希值:")
print(ripemd160_hashed_data)

# 替换区块链加解密算法为ECDSA和HMAC
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

class ECDSACryptography:
    def __init__(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key

    def sign(self, data):
        signature = self.private_key.sign(data, ec.ECDSA(Prehashed(hashes.SHA256())))
        return signature

    def verify(self, data, signature):
        try:
            self.public_key.verify(signature, data, ec.ECDSA(Prehashed(hashes.SHA256())))
            return True
        except Exception:
            return False

# 创建ECDSA密钥对
ecdsa_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
ecdsa_public_key = ecdsa_private_key.public_key()

# 创建ECDSA加解密实例
ecdsa_crypto = ECDSACryptography(ecdsa_private_key, ecdsa_public_key)

# 读取待签名的文本文件
with open("data_to_sign.txt", "rb") as file:
    data_to_sign = file.read()

# 对数据进行签名
signature = ecdsa_crypto.sign(data_to_sign)

# 保存签名到文件
with open("ecdsa_signature.txt", "wb") as file:
    file.write(signature)

# 验证签名
is_valid = ecdsa_crypto.verify(data_to_sign, signature)

# 打印验证结果
print("ECDSA Signature Verification Result:", is_valid)

# 替换混沌密码学加解密算法为Logistic映射和Chebyshev映射
from numpy import sin, cos, pi, exp, log

class LogisticMapEncryption:
    def __init(self, seed):
        self.seed = seed

    def encrypt(self, data):
        encrypted_data = []
        x = self.seed
        for byte in data:
            for _ in range(8):
                x = 4.0 * x * (1 - x)
                encrypted_data.append(byte ^ int(256 * x))
        return bytes(encrypted_data)

    def decrypt(self, encrypted_data):
        return self.encrypt(encrypted_data)  # Decryption is the same as encryption

class ChebyshevMapEncryption:
    def __init(self, seed):
        self.seed = seed

    def encrypt(self, data):
        encrypted_data = []
        x = self.seed
        for byte in data:
            for _ in range(8):
                x = cos(2 * cos(x))
                encrypted_data.append(byte ^ int(256 * x))
        return bytes(encrypted_data)

    def decrypt(self, encrypted_data):
        return self.encrypt(encrypted_data)  # Decryption is the same as encryption

# 创建两个不同的混沌密码学实例
logistic_map = LogisticMapEncryption(seed=0.5)
chebyshev_map = ChebyshevMapEncryption(seed=0.3)

# 读取待加密的文本文件
with open("chaos_input.txt", "rb") as file:
    plaintext = file.read()

# 使用第一个混沌密码学实例加密数据
encrypted_data_logistic_map = logistic_map.encrypt(plaintext)

# 使用第二个混沌密码学实例解密数据
decrypted_data_chebyshev_map = chebyshev_map.decrypt(encrypted_data_logistic_map)

# 保存解密后的数据到文件
with open("decrypted_logistic_map.txt", "wb") as file:
    file.write(decrypted_data_chebyshev_map)

# 打印解密后的数据
print("Logistic Map Decryption Result:")
print(decrypted_data_chebyshev_map)
