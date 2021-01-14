

# 定义函数，读取文件，获得所有的报文数据
# 参数：file_name 文件名称
# 返回值：所有报文构成的列表，列表每个元素代表一条报文
def read_inputs(file_name):
    # 打开文件，按行读取
    file = open(file_name, 'r', encoding='utf-8')
    lines = file.readlines()  # 按行读取文件内容
    file.close()
    # 去除换行符，构造返回结果列表
    packets = []  # 存放所有报文
    for line in lines:  # 遍历，去除换行符
        packets.append(line.strip('\n'))
    return packets


# 定义函数，由所有报文得到n-grams，此处还未做频率的统计处理
# 参数：第一个参数为n，便于尝试不同的n值；第二个参数为packets，即待划分的报文数据列表
# 返回值：所有 n-grams 构成的列表
def get_all_ngrams(n, packets):
    num = len(packets)  # 报文数目
    all_ngrams = []
    for i in range(num):  # 遍历所有报文
        message = packets[i]
        length = len(message)  # 长度
        repeat = length - n + 1  # 一条报文上的循环次数
        for i in range(repeat):
            all_ngrams.append(message[i:i+n])  # 都存入ngrams列表中
    return all_ngrams


# 定义函数，只保留频率排名靠前的一部分n-grams
# 参数：第一个参数为 P ，代表保留频率和满足阈值的一部分n-grams；第二个参数为ngrams，即所有n-grams的列表(get_all_ngrams的返回值)
# 返回值：频率和为P的 n-grams 列表
def get_allfreq_ngrams(P, ngrams):
    # 统计n-grams总数
    num = len(ngrams)
    print("所有报文的n-grams总数为：", num)
    # 先统计每种n-gram的出现频率，记录在字典中
    ngrams_dict = {}  # 存放各个n-gram的频率信息，无序的
    for i in ngrams:  # 遍历n-grams，统计每个出现频率
        ngrams_dict[i] = ngrams.count(i)/num  # key为n-gram, value为出现的频率
    # 对频率进行由大到小排序
    ordered = sorted(ngrams_dict.items(), key=lambda item: item[1], reverse=True)
    # 取出频率较高的一部分一部分
    allfreq_ngrams = []
    i = 0  # 当前取到第几个
    sum_p = 0  # 频率和
    while(sum_p < P):
        sum_p += ordered[i][1]
        allfreq_ngrams.append(ordered[i][0])
        i += 1
    return allfreq_ngrams


# 定义函数，由所有报文得到n-grams，此处还未做频率的统计处理
# 参数：第一个参数为n，便于尝试不同的n值；第二个参数为packets，即待划分的报文数据列表
# 返回值：列表套列表，大列表中每个元素是一个小列表，小列表对应一条报文的n-grams
def get_separate_ngrams(n, packets):
    sep_ngrams = []  # 用于存放不同报文的n-grams列表的大列表
    num = len(packets)
    for i in range(num):
        message = packets[i]
        length = len(message)
        message_ngrams = []  # 存储该报文n-grams的小列表
        repeat = length - n + 1  # 循环次数
        for j in range(repeat):
            message_ngrams.append(message[j:j+n])  # 小列表
        sep_ngrams.append(message_ngrams)  # 大列表
    return sep_ngrams


# 定义函数，每个报文只保留频率较高的n-grams
# 参数：第一个参数为 freq_ngrams，频数排名靠前的n-grams列表，即函数get_freq_ngrams的返回结果
#       第二个参数为 ngrams, 各个报文n-grams列表组成的列表，即函数get_separate_ngrams的返回结果，大列表套小列表形式
# 返回值：列表套列表，大列表中每个元素是一个小列表，小列表对应一条报文的高频n-grams
def get_sepfreq_ngrams(allfreq_ngrams, ngrams):
    sepfreq_ngrams = []  # 用于存放不同报文的高频n-grams列表的大列表
    num = len(ngrams)
    for i in range(num):  # 遍历报文
        message = ngrams[i]
        message_freq_ngrams = []  # 该报文高频n-grams的小列表
        for j in range(len(message)):
            if message[j] in allfreq_ngrams:
                message_freq_ngrams.append(message[j])  # 小列表
        sepfreq_ngrams.append(message_freq_ngrams)  # 大列表
    return sepfreq_ngrams


# 定义函数，将每个报文的高频n-grams保存到文件中,同一报文中n-grams空格隔开，每个报文占一行，末尾加换行符
# 参数：第一个参数 file_name为写入的txt文件名；第二个参数是写入的内容，即报文的高频n-grams列表组成的大列表
def save_freq_file(file_name, content):
    file = open(file_name, 'a')  # 打开文件，追加末尾
    num = len(content)  # 报文数目
    s = ""  # 所有报文的组合内容
    for i in range(num):
        message = content[i]  # 取出一条报文的n-grams列表
        t = "-".join(message)  # 用-组合起来，得到一条报文的内容，一般报文里没有-这个符号
        s = s + t + '\n'  # 去除每行末尾追加换行符
    file.write(s)  # 写入
    file.close()  # 关闭文件


# 主函数
if __name__ == "__main__":

    n = 4  # 初始化取值，n-gram中 n 的取值
    P = 0.1  # 保留的频率和，涉及的格式中随机内容较多，因此P值取的较小

    packets = read_inputs("inputs.txt")  # 读取文件，得到报文列表
    print("成功读取输入文件")

    all_ngrams = get_all_ngrams(n, packets)  # 从输入文件中获得所有n-grams的列表
    print("\n成功获得所有n-grams的小列表")

    allfreq_ngrams = get_allfreq_ngrams(P, all_ngrams)  # 排序，取出频率较高的一部分n-grams
    ngrams_num = len(allfreq_ngrams)
    print("\n保留频率和为%f的n-grams，共保留%d个" % (P, ngrams_num))
    print("保留的n-grams为：\n", allfreq_ngrams)

    sep_ngrams = get_separate_ngrams(n, packets)  # 从输入文件中获得n-grams的大列表套小列表的形式
    print("\n成功获得各个报文的n-grams列表")

    sepfreq_ngrams = get_sepfreq_ngrams(allfreq_ngrams, sep_ngrams)  # 保留每条报文中的高频n-grams
    print("\n成功获得各个报文的高频n-grams列表")

    save_freq_file("freq_ngrams.txt", sepfreq_ngrams)  # 保存报文的高频n-grams
    print("\n成功保存各个报文的高频n-grams到文件中")
