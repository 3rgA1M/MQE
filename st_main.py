import os
# streamlit run st_main.py
import random
# import mian
# import a
# import b
import streamlit as st

# 标题
st.title('Quantum Encryption Demo')

iv = os.urandom(16)
st.write(f"IV: {iv}")

# 创建按钮来生成密钥
if st.button('Generate RSA and ECC Keys'):
    # shared_key=mian.generate_keys(iv)
    st.write("RSA and ECC keys generated.")

# 显示加密和解密操作的按钮
plaintext = st.text_input("Enter plaintext to encrypt:", "Hello, Quantum World!")
# if st.button('Encrypt'):
    # encrypted_data = mian.quantum_encrypt(plaintext.encode(), shared_key)
    # st.write(f"Encrypted data: {encrypted_data}")

# if st.button('Decrypt'):
    # decrypted_data = mian.quantum_decrypt(encrypted_data, shared_key)
    # st.write(f"Decrypted text: {decrypted_data.decode()}")

st.subheader("OR")
# 文件上传
uploaded_file = st.file_uploader("Choose a file to encrypt")

if uploaded_file is not None:
    # 读取文件内容
    plaintext = uploaded_file.read()

    # 显示加密操作的按钮
    if st.button('Encrypt'):
        # encrypted_data = mian.quantum_encrypt(plaintext, shared_key)

        # 保存加密数据到一个文件，然后提供下载链接
        # with open("encrypted_data.txt", "wb") as f:
            # f.write(encrypted_data)
        st.download_button(
            label="Download Encrypted Data",
            data="encrypted_data.txt",
            file_name="encrypted_data.txt",
            mime="application/octet-stream"
        )

# 显示解密操作的按钮和文件上传
decrypted_file = st.file_uploader("Choose an encrypted file to decrypt")

if decrypted_file is not None:
    # 读取加密的文件内容
    encrypted_data = decrypted_file.read()

    if st.button('Decrypt'):
        # decrypted_data = mian.quantum_decrypt(encrypted_data, shared_key)
        
        # 保存解密数据到一个文件，然后提供下载链接
        # with open("decrypted_data.txt", "wb") as f:
            # f.write(decrypted_data)
        st.download_button(
            label="Download Decrypted Data",
            data="3125131613613",
            file_name="decrypted_data.txt",
            mime="text/plain"
        )
