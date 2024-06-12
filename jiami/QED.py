import streamlit as st
from qiskit import QuantumCircuit, transpile
import numpy as np
from io import BytesIO
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import base64

# 密钥生成
def generate_key(num_qubits):
    key = ""
    for i in range(num_qubits):
        bit = np.random.randint(2)
        key += str(bit)
    return key

# 加密消息
def encrypt_message(message, key, backend):
    num_qubits = len(key)
    qc = QuantumCircuit(num_qubits, num_qubits)
    for i in range(num_qubits):
        if key[i] == '1':
            qc.x(i)
    qc.barrier()
    for i in range(len(message)):
        if message[i] == '1':
            qc.x(i)
    qc.barrier()
    qc.measure(range(num_qubits), range(num_qubits))
    
    # 运行量子电路并获取结果
    transpiled_qc = transpile(qc, backend)
    result = backend.run(transpiled_qc).result()
    counts = result.get_counts()
    return list(counts.keys())[0]

# 保存量子状态向量
def save_statevector(statevector, filename):
    np.savetxt(filename, statevector.data)

# 解密消息
def decrypt_message(encrypted_message, key, backend):
    num_qubits = len(key)
    qc = QuantumCircuit(num_qubits, num_qubits)
    for i in range(num_qubits):
        if key[i] == '1':
            qc.x(i)
    qc.barrier()
    for i in range(len(encrypted_message)):
        if encrypted_message[i] == '1':
            qc.x(i)
    qc.barrier()
    qc.measure(range(num_qubits), range(num_qubits))
    
    # 运行量子电路并获取结果
    transpiled_qc = transpile(qc, backend)
    result = backend.run(transpiled_qc).result()
    counts = result.get_counts()
    return list(counts.keys())[0]

# 加密文件内容
def encrypt_file_contents(file_contents, key, backend, block_size):
    encrypted_blocks = []
    for i in range(0, len(file_contents), block_size):
        block = file_contents[i:i+block_size]
        encrypted_block = encrypt_message(block, key, backend)
        encrypted_blocks.append(encrypted_block)
    return ''.join(encrypted_blocks)

# 解密文件内容
def decrypt_file_contents(encrypted_file_contents, key, backend, block_size):
    decrypted_blocks = []
    for i in range(0, len(encrypted_file_contents), block_size):
        block = encrypted_file_contents[i:i+block_size]
        decrypted_block = decrypt_message(block, key, backend)
        decrypted_blocks.append(decrypted_block)
    return ''.join(decrypted_blocks)

# Streamlit 应用程序
key = None  # 初始化密钥
def main():
    

    st.title("File Encryption App")

    file = st.file_uploader("Upload a file")
    if file:
        st.write("File Uploaded Successfully!")

        # 读取文件内容
        file_contents = file.getvalue()

        global key  # 使用全局变量
        if key is None:
            # 生成新的密钥
            key = generate_key(8)  # 使用8位密钥
            st.write("Encryption Key:", key)  # 输出生成的密钥

        # 加密
        backend = Aer.get_backend('qasm_simulator')  # 获取后端
        encrypted_file_contents = encrypt_file_contents(file_contents, key, backend, block_size=8)

        # 下载加密后的文件
        st.write("Download the encrypted file:")
        download_link(encrypted_file_contents, "encrypted_file.txt")

    encrypted_file = st.file_uploader("Upload the encrypted file", type=['txt'])
    if encrypted_file:
        st.write("File Uploaded Successfully!")

        # 读取加密后的文件内容
        encrypted_file_contents = encrypted_file.getvalue().decode('utf-8').splitlines()

        # 解密
        if key:
            key_input = st.text_input("Enter the decryption key", value=key)
        else:
            key_input = st.text_input("Enter the decryption key")
        if st.button("Decrypt"):
            if key_input:
                backend = Aer.get_backend('qasm_simulator')
                decrypted_file_contents = decrypt_file_contents(encrypted_file_contents, key_input, backend, block_size=8)
                st.write("File Decrypted Successfully!")

                # 下载解密后的文件
                st.write("Download the decrypted file:")
                download_link(decrypted_file_contents, "decrypted_file.txt")
            else:
                st.warning("Please enter the decryption key.")

def download_link(data, filename):
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
