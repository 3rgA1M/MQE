# py 3.8使用
import numpy as np
import random
import librosa

# 音频文件路径
audio_file_path = 'C:\\Users\\lijinahe\\Desktop\\文件加密系统\\test.mp3'

print("读取音频成功,开始音频识别算法")
# 采样率（根据音频文件的实际采样率进行设置）
sample_rate = 44100

# 提取音频特征信息
audio, _ = librosa.load(audio_file_path, sr=sample_rate)

# 计算音频特征信息
amplitude = np.abs(audio)                        # 振幅/能量
spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sample_rate)[0]  # 谱带宽

print("特征信息提取成功，继续算法计算")

# 将所有特征信息合并成一个列表
all_features = np.concatenate([amplitude,  spectral_bandwidth])

# 随机排列特征信息
random.shuffle(all_features)
# =========================================================================
# 将特征信息转换为随机数字（以字符串形式）（所有的）
random_number_str = "".join(map(str, all_features))

# print("Random number:", random_number_str)   初代随机字符串太长简化
# 将字符串转换为7位的随机提取算法
def extract_seven_digits(string):
    digit_list = [char for char in string if char.isdigit()]
    if len(digit_list) < 7:
        return "The string contains less than 7 digits"
    random_indices = random.sample(range(len(digit_list)), 7)
    result = ''.join([digit_list[i] for i in random_indices])
    return result

# 输出随机数字
print("根据音频识别算法计算完成\n初代随机数如下：")

print(extract_seven_digits(random_number_str))

print("请输入初代随机数字：")
# 获取键盘输入的字符串
input_str = input()
# 将字符串赋给变量
value = input_str
plaintext = [int(x) for x in value]

# ================================================================================
#混合光学双稳模型加密算法
import numpy as np
from matplotlib import pyplot as plt
print("混合光学双稳模型加密算法加密开始")
# 定义参数
a = 1.8
b = -0.7
c = 0.1
d = -1.2

# 定义加密函数
def encrypt(plaintext, iterations, random_numbers):
    # 创建长度为iterations的列表，用于保存每一次迭代产生的混沌序列值
    sequence = np.zeros(iterations)

    # 初始化序列的初始值为随机数
    sequence[0] = np.random.random()

    # 生成混沌序列
    for i in range(1, iterations):
        # 计算下一个混沌序列值
        sequence[i] = ((a * sequence[i - 1] + b * sequence[i - 1] ** 2) + c * sequence[i - 1] ** 3 + d * sequence[i - 1] ** 4) % 1

    # 对明文进行加密
    ciphertext = np.zeros_like(plaintext)

    for i in range(len(plaintext)):
        # 使用混沌序列值与明文异或运算产生密文
        ciphertext[i] = plaintext[i] ^ sequence[i % iterations]  # 假设plaintext和ciphertext都是列表形式

    return ciphertext, random_numbers

# 测试加密和解密过程
iterations = 10000  # 迭代次数，也是混沌序列长度

# 输入明文==================================================================================
plaintext = plaintext # 以字符串形式输入明文数据

# 将明文转换为整数列表
plaintext = [ord(char) for char in plaintext if isinstance(char, str)]

# 生成随机数列表
random_numbers = []
for i in range(iterations):
    random_numbers.append(np.random.random())

# 加密
ciphertext, random_numbers = encrypt(plaintext, iterations, random_numbers)
    
# 输出提取的随机数
print("第二段加密结束")
print("最终随机数计算结果为：", random_numbers[:1])



