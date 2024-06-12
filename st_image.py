import streamlit as st
import cv2
import numpy as np
import random

def process_image(image_data):
    image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)
    hist_features = cv2.calcHist([image], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist_feature_values = [int(value) for value in hist_features.flatten()]
    feature_string = ', '.join(map(str, hist_feature_values))
    random_numbers = ''.join(random.choice('0123456789') for _ in range(10))
    return random_numbers

def generate_key(length):
    """
    生成一个模拟的量子密钥。

    参数:
    length (int): 密钥的长度，即生成的比特数。

    返回:
    str: 生成的密钥，是一个二进制字符串。
    """
    ket_0 = np.array([1, 0])  # |0>
    ket_1 = np.array([0, 1])  # |1>
    key = ""
    for _ in range(length):
        bit = np.random.randint(2)
        basis = np.random.choice([0, 1])
        outcome = measure_bit([ket_0, ket_1][basis], basis)
        key += str(outcome)
    return key

def measure_bit(qubit, basis):
    """
    测量一个量子位，根据指定的基。

    参数:
    qubit (np.array): 要测量的量子位的状态。
    basis (int): 使用的基，0 表示标准基，1 表示另一个基。

    返回:
    int: 测量结果，0 或 1。
    """
    ket_0 = np.array([1, 0])
    prob_0 = np.abs(np.dot(qubit, ket_0)) ** 2
    outcome = int(np.random.choice([0, 1], p=[prob_0, 1 - prob_0]))
    return outcome

st.title("图像加密系统")

uploaded_file = st.file_uploader("请选择一个图像文件", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    initial_random = process_image(uploaded_file)
    st.write("生成的初代随机数：", initial_random)

    key_length = len(initial_random)
    key = generate_key(key_length)
    final_random_number = int(key, 2)

    st.write("量子加密模块开始")
    st.write("加密方式：", "BB84")
    st.write("加密方式说明：", "基于量子位的BB84加密算法")
    st.write("生成的密钥：", key)
    st.write("最终随机数：", final_random_number)