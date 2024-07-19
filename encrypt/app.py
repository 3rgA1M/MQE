import os
import json
import streamlit as st
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from encryption import (
    encrypt_file_content, decrypt_file_content, generate_aes_key, generate_rsa_keys,
    LogisticMapEncryption, ChebyshevMapEncryption, encrypt_aes, decrypt_aes,
    encrypt_rsa, decrypt_rsa, generate_iv, generate_diffie_hellman_keys, generate_ecdh_keys
)
from bb84 import generate_bb84_key

# 包装加密方法以传递必要的参数，并保存密钥和参数
def wrap_aes_encrypt(data, key_dict):
    aes_key = generate_aes_key()
    iv = generate_iv()
    key_dict['aes_key'] = aes_key.hex()
    key_dict['aes_iv'] = iv.hex()
    return encrypt_aes(data, aes_key, iv)

def wrap_rsa_encrypt(data, key_dict):
    rsa_private_key, rsa_public_key = generate_rsa_keys()
    key_dict['rsa_private_key'] = rsa_private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    ).decode('utf-8')
    encrypted_aes_key = encrypt_rsa(bytes.fromhex(key_dict['aes_key']), rsa_public_key)
    key_dict['encrypted_aes_key'] = encrypted_aes_key.hex()
    return data

def wrap_bb84_encrypt(data, key_dict):
    bb84_key = generate_bb84_key()
    iv = generate_iv()
    key_dict['bb84_key'] = bb84_key.hex()
    key_dict['bb84_iv'] = iv.hex()
    return encrypt_aes(data, bb84_key, iv)

def wrap_ecdh_encrypt(data, key_dict):
    ecdh_private_key, ecdh_public_key = generate_ecdh_keys()
    shared_key = ecdh_private_key.exchange(ec.ECDH(), ecdh_public_key)
    key_dict['ecdh_private_key'] = ecdh_private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    ).decode('utf-8')
    key_dict['ecdh_public_key'] = ecdh_public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    return encrypt_aes(data, shared_key[:32], generate_iv())

def wrap_elgamal_encrypt(data, key_dict):
    # 使用 ECDH 代替 ElGamal
    return wrap_ecdh_encrypt(data, key_dict)

# 包装解密方法以传递必要的参数
def wrap_aes_decrypt(data, key_dict):
    aes_key = bytes.fromhex(key_dict['aes_key'])
    iv = bytes.fromhex(key_dict['aes_iv'])
    return decrypt_aes(data, aes_key)

def wrap_rsa_decrypt(data, key_dict):
    rsa_private_key = serialization.load_pem_private_key(
        key_dict['rsa_private_key'].encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    encrypted_aes_key = bytes.fromhex(key_dict['encrypted_aes_key'])
    aes_key = decrypt_rsa(encrypted_aes_key, rsa_private_key)
    key_dict['aes_key'] = aes_key.hex()
    return data

def wrap_bb84_decrypt(data, key_dict):
    bb84_key = bytes.fromhex(key_dict['bb84_key'])
    iv = bytes.fromhex(key_dict['bb84_iv'])
    return decrypt_aes(data, bb84_key)

def wrap_ecdh_decrypt(data, key_dict):
    ecdh_private_key = serialization.load_pem_private_key(
        key_dict['ecdh_private_key'].encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    ecdh_public_key = serialization.load_pem_public_key(
        key_dict['ecdh_public_key'].encode('utf-8'),
        backend=default_backend()
    )
    shared_key = ecdh_private_key.exchange(ec.ECDH(), ecdh_public_key)
    return decrypt_aes(data, shared_key[:32])

def wrap_elgamal_decrypt(data, key_dict):
    # 使用 ECDH 代替 ElGamal
    return wrap_ecdh_decrypt(data, key_dict)

# Streamlit 应用
def main():
    st.title("文件加密系统")
    st.header("上传文件并选择加密或解密方法")

    mode = st.selectbox("选择模式", ["加密", "解密"])

    if mode == "加密":
        file = st.file_uploader("上传要加密的文件")

        methods = {
            "AES": wrap_aes_encrypt,
            "RSA": wrap_rsa_encrypt,
            "BB84": wrap_bb84_encrypt,
            "Logistic Map": LogisticMapEncryption(seed=0.5).encrypt,
            "Chebyshev Map": ChebyshevMapEncryption(seed=0.3).encrypt,
            "ECDH": wrap_ecdh_encrypt,
            "ElGamal": wrap_elgamal_encrypt  # 使用 ECDH 代替 ElGamal
        }

        selected_methods = st.multiselect(f"选择加密方法（最多三个）", list(methods.keys()))

        if file and selected_methods:
            if len(selected_methods) > 3:
                st.error("最多选择三个加密方法")
            else:
                # 读取文件内容
                file_content = file.read()
                file_name = file.name

                # 初始化密钥和参数字典
                key_dict = {}

                # 选择的加密方法
                selected_encrypt_methods = [(methods[method], {'key_dict': key_dict}) for method in selected_methods]

                # 调用加密函数
                encrypted_data = encrypt_file_content(file_content, selected_encrypt_methods)

                # 显示加密结果
                st.write("加密数据长度:", len(encrypted_data))

                # 保存加密后的文件
                encrypted_file_path = os.path.join("temp", "encrypted_data.bin")
                with open(encrypted_file_path, "wb") as f:
                    f.write(encrypted_data)

                # 保存密钥和参数
                keys_params_file_path = os.path.join("temp", "keys_params.json")
                with open(keys_params_file_path, "w") as f:
                    json.dump(key_dict, f)

                # 导出加密数据和密钥参数
                export_data = {
                    "file_name": file_name,
                    "encrypted_data": encrypted_data.hex(),
                    "keys_params": key_dict
                }
                export_file_path = os.path.join("temp", "encrypted_export.json")
                with open(export_file_path, "w") as f:
                    json.dump(export_data, f)

                st.success("文件已成功加密并保存！")
                st.download_button(label="下载加密文件", data=json.dumps(export_data), file_name="encrypted_export.json", mime="application/json")

    elif mode == "解密":
        encrypted_file = st.file_uploader("导入加密文件", type=["json"])

        decrypt_methods = {
            "AES": wrap_aes_decrypt,
            "RSA": wrap_rsa_decrypt,
            "BB84": wrap_bb84_decrypt,
            "Logistic Map": LogisticMapEncryption(seed=0.5).decrypt,
            "Chebyshev Map": ChebyshevMapEncryption(seed=0.3).decrypt,
            "ECDH": wrap_ecdh_decrypt,
            "ElGamal": wrap_elgamal_decrypt  # 使用 ECDH 代替 ElGamal
        }

        selected_methods = st.multiselect(f"选择解密方法（最多三个）", list(decrypt_methods.keys()))

        if encrypted_file and selected_methods:
            if len(selected_methods) > 3:
                st.error("最多选择三个解密方法")
            else:
                # 读取导入的加密文件
                import_data = json.load(encrypted_file)
                file_name = import_data["file_name"]
                encrypted_data = bytes.fromhex(import_data["encrypted_data"])
                key_dict = import_data["keys_params"]

                # 选择的解密方法
                selected_decrypt_methods = [(decrypt_methods[method], {'key_dict': key_dict}) for method in selected_methods]

                # 调用解密函数
                decrypted_data = decrypt_file_content(encrypted_data, selected_decrypt_methods)

                # 显示解密结果
                st.write("解密数据长度:", len(decrypted_data))

                # 保存解密后的文件
                decrypted_file_path = os.path.join("temp", file_name)
                with open(decrypted_file_path, "wb") as f:
                    f.write(decrypted_data)

                st.success("文件已成功解密并保存！")
                st.download_button(label="下载解密文件", data=decrypted_data, file_name=file_name, mime="application/octet-stream")

if __name__ == "__main__":
    if not os.path.exists("temp"):
        os.makedirs("temp")
    main()