import streamlit as st
import numpy as np
import random
import librosa
from matplotlib import pyplot as plt

# 音频处理和特征提取
def process_audio(audio_file):
    sample_rate = 44100
    audio, _ = librosa.load(audio_file, sr=sample_rate)
    amplitude = np.abs(audio)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sample_rate)[0]
    all_features = np.concatenate([amplitude, spectral_bandwidth])
    random.shuffle(all_features)
    random_number_str = "".join(map(str, all_features))
    return extract_seven_digits(random_number_str)

# 提取7位数字
def extract_seven_digits(string):
    digit_list = [char for char in string if char.isdigit()]
    if len(digit_list) < 7:
        return "Error: Less than 7 digits"
    random_indices = random.sample(range(len(digit_list)), 7)
    result = ''.join([digit_list[i] for i in random_indices])
    return result

# 混合光学双稳模型加密算法
def encrypt(plaintext, iterations):
    a = 1.8
    b = -0.7
    c = 0.1
    d = -1.2
    sequence = np.zeros(iterations)
    sequence[0] = np.random.random()
    for i in range(1, iterations):
        sequence[i] = ((a * sequence[i - 1] + b * sequence[i - 1] ** 2) + c * sequence[i - 1] ** 3 + d * sequence[i - 1] ** 4) % 1
    
    ciphertext = np.zeros_like(plaintext)
    for i in range(len(plaintext)):
        ciphertext[i] = int(plaintext[i]) ^ int(sequence[i % iterations] * 1000)

    return ciphertext

# Streamlit 应用
st.title('音频文件加密系统')

uploaded_file = st.file_uploader("请选择一个音频文件 (.mp3)", type="mp3")
if uploaded_file is not None:
    initial_random = process_audio(uploaded_file)
    st.write("生成的初代随机数：", initial_random)

    input_text = st.text_input("请输入初代随机数字：")
    if st.button("加密"):
        plaintext = [ord(char) for char in input_text]
        iterations = 10000
        ciphertext = encrypt(plaintext, iterations)
        st.write("加密结果：", ciphertext)