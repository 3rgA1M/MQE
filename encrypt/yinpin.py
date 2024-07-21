# 导入所需的库
import numpy as np
import random
import librosa
from matplotlib import pyplot as plt

# 音频文件路径（转换后的音频文件路径）
audio_file_path = r"C:\xiangmu\python\suijimiyao\aaa\3.mp3"


print("读取音频成功,开始音频识别算法")

# 采样率（根据音频文件的实际采样率进行设置）
sample_rate = 44100

# 提取音频特征信息
try:
    audio, _ = librosa.load(audio_file_path, sr=sample_rate)
except Exception as e:
    print(f"读取音频文件失败: {e}")
    exit()

# 计算音频特征信息
amplitude = np.abs(audio)  # 振幅/能量
spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sample_rate)[0]  # 谱带宽
mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate)  # 梅尔频率倒谱系数
chroma = librosa.feature.chroma_stft(y=audio, sr=sample_rate)  # 色度特征

print("特征信息提取成功，继续算法计算")

# 将所有特征信息合并成一个列表
all_features = np.concatenate([amplitude, spectral_bandwidth, mfcc.flatten(), chroma.flatten()])

# 随机排列特征信息
random.shuffle(all_features)

# 将特征信息转换为随机数字（以字符串形式）
random_number_str = "".join(map(str, all_features.astype(int)))

# 提取7位随机数字
def extract_seven_digits(string):
    digit_list = [char for char in string if char.isdigit()]
    if len(digit_list) < 7:
        return "The string contains less than 7 digits"
    random_indices = random.sample(range(len(digit_list)), 7)
    result = ''.join([digit_list[i] for i in random_indices])
    return result

# 输出随机数字
print("根据音频识别算法计算完成\n初代随机数如下：")
initial_random_number = extract_seven_digits(random_number_str)
print(initial_random_number)

print("请输入初代随机数字：")
# 获取键盘输入的字符串
input_str = input()

# 将字符串转换为整数列表
try:
    plaintext = [int(x) for x in input_str]
except ValueError:
    print("输入必须是数字!")
    exit()

print("混合光学双稳模型加密算法加密开始")

# 定义加密函数
def encrypt(plaintext, iterations):
    # 检查输入数据的类型
    if not isinstance(plaintext, list) or not all(isinstance(x, int) for x in plaintext):
        raise ValueError("明文必须是整数列表!")

    # 创建长度为iterations的列表，用于保存每一次迭代产生的混沌序列值
    sequence = np.zeros(iterations)

    # 初始化序列的初始值为随机数
    sequence[0] = np.random.random()

    # 定义参数
    a = 1.8
    b = -0.7
    c = 0.1
    d = -1.2

    # 生成混沌序列
    for i in range(1, iterations):
        # 计算下一个混沌序列值
        sequence[i] = ((a * sequence[i - 1] + b * sequence[i - 1] ** 2) + c * sequence[i - 1] ** 3 + d * sequence[i - 1] ** 4) % 1

    # 对明文进行加密
    ciphertext = np.zeros_like(plaintext)

    for i in range(len(plaintext)):
        # 使用混沌序列值与明文异或运算产生密文
        ciphertext[i] = plaintext[i] ^ int(sequence[i % iterations] * 1000)  # 将序列值缩放到整数范围内

    return ciphertext.tolist()

# 测试加密和解密过程
iterations = 10000  # 迭代次数，也是混沌序列长度

# 加密
try:
    ciphertext = encrypt(plaintext, iterations)
except ValueError as e:
    print(e)
    exit()

# 输出提取的随机数
print("第二段加密结束")
print("最终随机数计算结果为：", ciphertext[:1])
