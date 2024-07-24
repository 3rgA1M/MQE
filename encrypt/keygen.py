import streamlit as st
import cv2
import numpy as np
import sounddevice as sd
import scipy.fftpack
import random
import io
import wave

# 图像识别：捕捉图像并提取随机数据
def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Failed to open camera")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise Exception("Failed to capture image")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    random_data = np.random.choice(thresh.flatten(), 256).astype(np.uint8)
    return frame, random_data

# 音频处理：捕捉环境噪声并提取随机数据
def capture_audio(duration=1, fs=44100):
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()
    recording = np.int16(recording * 32767)  # 将音频数据转换为16位整数格式
    fft_data = scipy.fftpack.fft(recording.flatten())
    random_data = np.random.choice(np.abs(fft_data), 256).astype(np.uint8)
    return recording, random_data, fs

# 生成初代密钥
def generate_initial_key(image_data, audio_data):
    combined_data = np.bitwise_xor(image_data, audio_data)
    initial_key = ''.join(format(x, '02x') for x in combined_data)
    return initial_key

# BB84量子加密实现
def bb84_quantum_encrypt(key):
    # 生成随机基（0 或 1）
    bases = [random.randint(0, 1) for _ in key]
    
    # 生成随机比特
    bits = [random.randint(0, 1) for _ in key]
    
    # 对比特进行编码
    encoded_bits = []
    for bit, base in zip(bits, bases):
        if base == 0:  # 直线基
            encoded_bits.append(bit)
        else:  # 对角基
            encoded_bits.append(1 - bit)
    
    # 模拟量子传输和测量（Alice 和 Bob 的基相同才保留比特）
    received_bits = []
    for bit, base in zip(encoded_bits, bases):
        if random.randint(0, 1) == base:
            received_bits.append(bit)
    
    # 生成密钥（Alice 和 Bob 的基相同的比特）
    final_key = ''.join(map(str, received_bits))
    return final_key

# 混沌加密实现
def logistic_map(x, r=3.99):
    return r * x * (1 - x)

def chaotic_encrypt(key):
    # 初始条件
    x = 0.5
    encrypted_key = ""
    for char in key:
        x = logistic_map(x)
        # 生成混沌序列
        chaotic_value = int(x * 256) % 256
        # 对每个字符进行异或运算
        encrypted_char = chr(ord(char) ^ chaotic_value)
        encrypted_key += encrypted_char
    return encrypted_key

# 将加密密钥转换为十六进制字符串
def key_to_hex(key):
    return ''.join(format(ord(char), '02x') for char in key)

# 将音频数据保存为WAV格式
def save_audio_to_wav(audio_data, fs):
    audio_bytes = io.BytesIO()
    with wave.open(audio_bytes, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16位音频
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())
    audio_bytes.seek(0)
    return audio_bytes

# Streamlit应用程序
def main():
    st.title("密钥生成系统")

    # 捕捉图像和音频数据的按钮
    if st.button("捕捉图像和音频"):
        try:
            st.write("捕捉图像中...")
            image, image_data = capture_image()
            st.image(image, caption="捕获的图像", use_column_width=True)
            st.write("图像捕捉成功")

            st.write("捕捉音频中...")
            audio, audio_data, fs = capture_audio()
            audio_bytes = save_audio_to_wav(audio, fs)
            st.audio(audio_bytes, format='audio/wav')
            st.write("音频捕捉成功")

            # 生成初代密钥
            initial_key = generate_initial_key(image_data, audio_data)
            st.write("初代密钥生成成功")

            # 进行BB84量子加密
            quantum_encrypted_key = bb84_quantum_encrypt(initial_key)
            st.write("BB84量子加密成功")

            # 进行混沌加密
            final_encrypted_key = chaotic_encrypt(quantum_encrypted_key)
            st.write("混沌加密成功")

            # 转换为十六进制字符串
            hex_encrypted_key = key_to_hex(final_encrypted_key)
            st.success(f"最终加密密钥（十六进制）: {hex_encrypted_key}")
        except Exception as e:
            st.error(f"发生错误: {e}")

if __name__ == "__main__":
    main()