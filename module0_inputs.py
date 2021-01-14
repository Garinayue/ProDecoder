import uuid  # 用于生成十六进制
import random


# 各字段的含义以及初值，全局变量

# 四个固定的开始字节，有四种不同格式，main函数中赋值
head = ""

# 两固定字节常量，指示来源，有四种不同格式，main函数中赋值
src_indicator = ""

# 四字节变量，代表源地址，由函数随机生成
src = ""

# 两固定字节常量，指示目的，有四种不同格式，main函数中赋值
dst_indicator = ""

# 四字节变量，代表目的地址，由函数随机生成
dst = ""

content_indicator = "ffff"  # 两字节常量，表示后面是正文
boo = "00"  # 一字节布尔型变量，取值0或1
length = "00"  # 一字节变量，代表正文长度
content = ""  # 长度由length决定，正文内容


# 定义函数，用于随机生成四字节的变量
# 参数：无
# 返回值：随机生成的十六进制形式的四个字节
def get_four_bytes():
    res = str(uuid.uuid4())  # 形如 02680d49-e91d-4ccb-a4b9-8a05c3ed86e9
    res = res.replace('-', '')  # 形如 02680d49e91d4ccba4b98a05c3ed86e9
    res = res[:8]  # 取前4个字节
    return res


# 定义函数，用于随机生成布尔型变量
# 参数：无
# 返回值：随机生成的布尔值形式的一个字节
def get_bool_byte():
    res = random.getrandbits(1)  # 随机生成整型0或1
    if res == 0:  # 转化为十六进制形式的字符串
        return "00"
    else:
        return "01"


# 定义函数，用于随机生成一个字节的长度字段
# 参数：无
# 返回值：随机生成的十六进制形式的一个字节
def get_one_byte():
    res = str(uuid.uuid4())  # 形如 02680d49-e91d-4ccb-a4b9-8a05c3ed86e9
    res = res.replace('-', '')  # 形如 02680d49e91d4ccba4b98a05c3ed86e9
    res = res[:2]  # 取前1个字节
    return res


# 定义函数，用于随机生成指定长度正文内容 （太长了导致后面速度太慢，所以取长度的一半）
# 参数：是字符串形式的十六进制
# 返回值：指定长度的十六进制构成的字符串
def get_content(str_len):
    length = int(str_len, 16) // 2  # 字符串形式的十六进制转化为十进制数字，并变成一半
    res = ""  # 初始化返回结果
    repeat = length // 16 + 1  # 一次可以得到16个字节，计算循环多少次，
    for i in range(repeat):  # 循环，每次生成16个字节，并拼接起来
        tmp = str(uuid.uuid4())
        tmp = tmp.replace('-', '')  # 可以生成16字节
        res += tmp  # 字符串拼接
    res = res[:length*2]  # 取 length 个字节，乘2因为一个字节用两个十六进制表示
    return res


# 定义函数，用于批量生成报文
# 参数：number，代表产生的报文数量
# 返回值：所有报文组成的列表
def get_inputs(number, head, src_indicator, dst_indicator):
    packets = []  # 列表，用于存储所有报文，初始化为空
    for i in range(number):
        src = get_four_bytes()
        dst = get_four_bytes()
        boo = get_bool_byte()
        length = get_one_byte()
        content = get_content(length)
        # 组合得到消息
        message = head + src_indicator + src + dst_indicator + dst + content_indicator + boo + length + content
        packets.append(message)
    return packets


# 定义函数，将报文保存到文件中
# 参数：第一个参数 file_name为写入的txt文件名；第二个参数是写入的内容，即报文列表
def save_file(file_name, content_list):
    file = open(file_name, 'a')  # 打开文件，追加末尾
    num = len(content_list)
    print("共有%d条报文数据" % (num))
    s = ""
    for i in range(num):
        s = s + content_list[i] + '\n'
    file.write(s)  # 写入
    file.close()  # 关闭文件
    print("保存文件成功")


# 主函数，按照格式批量生成报文，并写入文件中
if __name__ == "__main__":

    num = 100  # 定义每种格式的报文数目

    # 第一种格式
    head = "68656164"
    src_indicator = "6672"
    dst_indicator = "746f"
    packets = get_inputs(num, head, src_indicator, dst_indicator)  # 得到num条报文，列表形式
    save_file("inputs.txt", packets)  # 写入文件

    # 第二种格式
    head = "12345678"
    src_indicator = "3344"
    dst_indicator = "8899"
    packets = get_inputs(num, head, src_indicator, dst_indicator)  # 得到num条报文，列表形式
    save_file("inputs.txt", packets)  # 写入文件

    # 第三种格式
    head = "19991023"
    src_indicator = "0915"
    dst_indicator = "0614"
    packets = get_inputs(num, head, src_indicator, dst_indicator)  # 得到num条报文，列表形式
    save_file("inputs.txt", packets)  # 写入文件

    # 第四种格式
    head = "56785678"
    src_indicator = "2020"
    dst_indicator = "1226"
    packets = get_inputs(num, head, src_indicator, dst_indicator)  # 得到num条报文，列表形式
    save_file("inputs.txt", packets)  # 写入文件
