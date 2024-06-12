import os
import streamlit as st

# Assuming your cryptographic functions are in a module named 'main'
import mian

# Title of the app
st.title('Quantum Encryption Demo')

# Generate a random Initialization Vector
iv = os.urandom(16)
st.write(f"IV: {iv.hex()}")  # Display the IV in hexadecimal format

# Button to generate RSA and ECC keys
if st.button('Generate RSA and ECC Keys'):
    shared_key = mian.generate_keys(iv)
    st.session_state['shared_key'] = shared_key  # Store key in session state
    st.write("RSA and ECC keys generated.")

# Text input for plaintext
plaintext = st.text_input("Enter plaintext to encrypt:", "Hello, Quantum World!")

# Encrypt button
if st.button('Encrypt'):
    if 'shared_key' in st.session_state:
        encrypted_data = mian.quantum_encrypt(plaintext.encode(), st.session_state['shared_key'])
        st.session_state['encrypted_data'] = encrypted_data  # Store encrypted data in session state
        st.write(f"Encrypted data: {encrypted_data}")
    else:
        st.error("No keys generated. Please generate keys first.")

# Decrypt button
if st.button('Decrypt'):
    if 'encrypted_data' in st.session_state and 'shared_key' in st.session_state:
        decrypted_data = mian.quantum_decrypt(st.session_state['encrypted_data'], st.session_state['shared_key'])
        st.write(f"Decrypted text: {decrypted_data.decode()}")

st.subheader("OR")

# File uploader for encryption
uploaded_file = st.file_uploader("Choose a file to encrypt")
if uploaded_file is not None:
    file_data = uploaded_file.read()
    if st.button('Encrypt File'):
        if 'shared_key' in st.session_state:
            encrypted_file_data = mian.quantum_encrypt(file_data, st.session_state['shared_key'])
            st.download_button(
                label="Download Encrypted Data",
                data=encrypted_file_data,
                file_name="encrypted_data.txt",
                mime="application/octet-stream"
            )
        else:
            st.error("No keys generated. Please generate keys first.")

# File uploader for decryption
decrypted_file = st.file_uploader("Choose an encrypted file to decrypt")
if decrypted_file is not None:
    encrypted_file_data = decrypted_file.read()
    if st.button('Decrypt File'):
        if 'shared_key' in st.session_state:
            decrypted_file_data = mian.quantum_decrypt(encrypted_file_data, st.session_state['shared_key'])
            st.download_button(
                label="Download Decrypted Data",
                data=decrypted_file_data,
                file_name="decrypted_data.txt",
                mime="text/plain"
            )
        else:
            st.error("No keys generated. Please generate keys first.")