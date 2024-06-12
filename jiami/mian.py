# 导入所需库
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives import hashes
from qiskit import QuantumCircuit, Aer, execute

import random

# 生成一个16字节的随机初始向量（IV）
iv = os.urandom(16)
print("IV 是:", iv)

# 生成用于密钥交换的 RSA 密钥对
private_rsa_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_rsa_key = private_rsa_key.public_key()

# 生成用于数据加密的 ECC 密钥对
private_ecc_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
public_ecc_key = private_ecc_key.public_key()

# 使用 RSA 加密 AES 和 TripleDES 密钥进行密钥交换
aes_key = os.urandom(16)
encrypted_aes_key = public_rsa_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA512()),  # 使用 SHA-512 作为 MGF1
        algorithm=hashes.SHA512(),  # 使用 SHA-512 作为 OAEP
        label=None
    )
)

# 使用 RSA 加密 TripleDES 密钥进行密钥交换
triple_des_key = os.urandom(8)
encrypted_triple_des_key = public_rsa_key.encrypt(
    triple_des_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA512()),  # 使用 SHA-512 作为 MGF1
        algorithm=hashes.SHA512(),  # 使用 SHA-512 作为 OAEP
        label=None
    )
)

# 定义加密算法
algorithm_aes = algorithms.AES(aes_key)
algorithm_3des = algorithms.TripleDES(triple_des_key)

# 定义 B92 量子密钥分发算法
def run_b92():
    # 创建一个量子电路，执行 B92 算法的步骤
    qc = QuantumCircuit(2, 1)
    
    # 随机生成一个比特作为基态的选择，0或1表示基态
    alice_basis = [random.choice([0, 1]) for _ in range(2)]

    # 随机生成一个比特，用于确定发送的比特值，0或1表示比特值
    alice_bits = [random.choice([0, 1]) for _ in range(2)]

    # 在量子电路中加入 Hadamard 门或标准门，基于 Alice 的选择
    for i in range(2):
        if alice_basis[i] == 0:  # Hadamard
            qc.h(i)
        if alice_bits[i] == 1:
            qc.x(i)

    # 模拟量子电路
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1)

    # 获取测量结果
    result = job.result()
    counts = result.get_counts()

    # 根据测量结果，Alice 和 Bob 得出共享的密钥
    shared_key = ""
    for key in counts.keys():
        shared_key = key

    return shared_key

# 定义 E91 量子密钥分发算法
def run_e91():
    # 创建一个量子电路，执行 E91 算法的步骤
    qc = QuantumCircuit(3, 2)
    
    # Alice 随机生成一个比特作为基态的选择，0或1表示基态
    alice_basis = [random.choice([0, 1]) for _ in range(3)]

    # Bob 随机生成一个比特，用于确定发送的比特值，0或1表示比特值
    alice_bits = [random.choice([0, 1]) for _ in range(3)]

    # 在量子电路中加入 Hadamard 门或标准门，基于 Alice 的选择
    for i in range(3):
        if alice_basis[i] == 0:  # Hadamard
            qc.h(i)
        if alice_bits[i] == 1:
            qc.x(i)

    # 模拟量子电路
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1)

    # 获取测量结果
    result = job.result()
    counts = result.get_counts()

    # 根据测量结果，Alice 和 Bob 得出共享的密钥
    shared_key = ""
    for key in counts.keys():
        shared_key = key

    return shared_key

# 执行 B92 算法并获取共享密钥
b92_shared_key = run_b92()

# 执行 E91 算法并获取共享密钥
e91_shared_key = run_e91()

# 使用共享的量子密钥对数据进行加密和解密
def quantum_encrypt(data, shared_key):
    # 使用 shared_key 对数据进行量子加密
    # 这里可以使用共享的密钥执行量子加密操作
    encrypted_data = data  # 假设这里进行了量子加密
    return encrypted_data

def quantum_decrypt(encrypted_data, shared_key):
    # 使用 shared_key 对数据进行量子解密
    # 这里可以使用共享的密钥执行量子解密操作
    decrypted_data = encrypted_data  # 假设这里进行了量子解密
    return decrypted_data

# 示例明文数据
plaintext = b"Hello, Quantum World!"

# 使用 B92 或 E91 算法获取共享的量子密钥
shared_key = b92_shared_key  # 这里选择 B92 共享的密钥

# 加密数据
encrypted_data = quantum_encrypt(plaintext, shared_key)

# 解密数据
decrypted_data = quantum_decrypt(encrypted_data, shared_key)

# 指定输入和输出文件路径
input_file = "input.txt"
output_file = "output.txt"

# 将加密后的数据写入输出文件
with open(output_file, 'wb') as file:
    file.write(encrypted_data)

# 从输入文件中读取加密后的数据
with open(output_file, 'rb') as file:
    encrypted_data = file.read()

# 使用共享的密钥进行解密
decrypted_data = quantum_decrypt(encrypted_data, shared_key)

# 打印解密后的数据
print("解密后的数据:")
print(decrypted_data)

# 使用 SHA-384 对明文进行哈希
digest = hashes.Hash(hashes.SHA384(), backend=default_backend())
digest.update(plaintext)
hash_value = digest.finalize()

# 使用 AES 和 TripleDES 进行加密
ciphertext_aes = encrypt(plaintext, algorithm_aes, iv)
ciphertext_3des = encrypt(ciphertext_aes, algorithm_3des, iv)

# 将加密数据和哈希写入输出文件
with open(output_file, 'wb') as file:
    file.write(ciphertext_3des)
    file.write(hash_value)

# 解密数据（反向过程）
decrypted_aes = decrypt(ciphertext_3des, algorithm_3des, iv)
decrypted_plaintext = decrypt(decrypted_aes, algorithm_aes, iv)

# 验证解密后的明文的哈希值
digest = hashes.Hash(hashes.SHA384(), backend=default_backend())
digest.update(decrypted_plaintext)
decrypted_hash_value = digest.finalize()

if decrypted_hash_value == hash_value:
    print("数据完整性验证成功。")
else:
    print("数据完整性受损。")

# 打印解密后的明文
print("解密后的文本:")
print(decrypted_plaintext)



def generate_keys(iv):
    # todo: implement
    return
