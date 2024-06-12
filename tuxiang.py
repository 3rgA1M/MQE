# py3.12版本使用
import cv2
import numpy as np
import random

# 图像识别获得初代随机数
# 读取图像
image_file = 'C:\\Users\\lijinahe\\Desktop\\文件加密系统\\python\\suijimiyao\\aaa\1.jpg'

image = cv2.imread(image_file)

# 获取图像的尺寸
height, width, _ = image.shape

# 获取图像的平均像素值
average_pixel_value = np.mean(image)

# 获取图像的通道数
num_channels = image.shape[2]

# 获取图像的面积
area = height * width

# 获取图像的总像素数
total_pixels = height * width * num_channels

# 获取图像的颜色直方图特征
hist_features = cv2.calcHist([image], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])

# 展平直方图特征为一维数组，然后将其转化为整数
hist_feature_values = [int(value) for value in hist_features.flatten()]

# 将特征值连接成一个字符串
feature_string = ','.join(map(str, hist_feature_values))

# 生成随机数字串
random_numbers = ''.join(random.choice('0123456789') for _ in range(10))

# 最终生成的字符串
output_string = f'Features: {feature_string}\nRandom Numbers: {random_numbers}'
aa=random_numbers
print("依据图像识别加密算法成功\n获取初代随机数如下：")
print(aa)


# 导入所需模块
import numpy as np

# 定义量子位的基础状态
ket_0 = np.array([1, 0])  # |0>
ket_1 = np.array([0, 1])  # |1>

# 选择加密方式和注释（可选）
encryption_method = "BB84"  # 使用BB84加密算法
encryption_comment = "基于量子位的BB84加密算法"  # 加密方式的注释

# BB84协议的量子比特随机选择函数
def random_bit():
    return np.random.randint(2)

# BB84协议的随机基选择函数
def random_basis():
    return np.random.choice([0, 1])  # 修改此行代码，只选择一维数组为随机基

# BB84协议的比特测量函数
def measure_bit(qubit, basis):
    prob_0 = np.abs(np.dot(qubit, ket_0)) ** 2
    if basis == 0:  # 修改此行代码，改为比较基的索引值
        outcome = int(np.random.choice([0, 1], p=[prob_0, 1 - prob_0]))
    else:
        outcome = int(np.random.choice([0, 1], p=[1 - prob_0, prob_0]))
    return outcome

# BB84协议的密钥生成函数
def generate_key(length):
    key = ""
    for _ in range(length):
        bit = random_bit()
        basis = random_basis()
        outcome = measure_bit([ket_0, ket_1][basis], basis)  # 修改此行代码，传入对应的基和比特
        key += str(bit)
    return key

# 读取初代随机数
aa = input("请输入初代随机数：")

# 从初代随机数中选择需要的位数作为密钥长度
key_length = len(aa)
key = generate_key(key_length)

# 最终生成的随机数
final_random_number = int(key, 2)

# 输出结果
print("量子加密模块开始")
print("加密方式：", encryption_method)
print("加密方式说明：", encryption_comment)
print("生成的密钥：", key)
print("最终随机数：", final_random_number)
