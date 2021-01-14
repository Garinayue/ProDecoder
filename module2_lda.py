import numpy as np
import lda


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


# 定义函数，对高频n-grams列表预处理，为每个 n-gram 赋予编号，报文使用 n-gram 编号的列表表示，组织训练数据矩阵
# 参数：各个报文的高频n-grams列表，大列表套小列表形式
# 返回值：四个
# 1. new_packets  所有报文的编号列表，每个报文对应一个存放n-gram编号的小列表
# 2. ngram2id  字典，键为 n-gram，值为 id
# 3. id2ngram  字典，键为 id，值为 n-gram
# 4. X  组织好的训练数据，每一行代表一个报文，每一列为一个n-gram，(i, j)代表第i个文档中第j个n-gram出现的次数
def preprocess(packets):
    # 初始化
    ngram2id = {}  # 字典，键为 n-gram，值为 id
    id2ngram = {}  # 字典，键为 id，值为 n-gram
    new_packets = []  # 存放所有报文的编号列表，每个报文对应一个存放n-gram编号的小列表
    currentPacket = []  # 当前报文的编号列表
    currentId = 0  # n-gram当前编号到哪个数字了
    # 对n-gram和报文进行编号
    for message in packets:  # 遍历每个报文
        for ngram in message:   # 遍历报文的每个n-gram
            if ngram in ngram2id:  # 如果该n-gram已经编号过
                currentPacket.append(ngram2id[ngram])  # 直接记录该报文的n-gram编号即可
            else:  # 如果该n-gram未编号过
                ngram2id[ngram] = currentId  # 先分别在两个列表中对该n-gram进行编号
                id2ngram[currentId] = ngram
                currentPacket.append(currentId)  # 再记录报文的n-gram编号
                currentId += 1
        new_packets.append(currentPacket)  # 存储该报文的编号列表
        currentPacket = []
    # 组织训练数据
    row = len(packets)
    col = len(ngram2id)
    X = np.zeros([row, col], dtype=int)  # 要指定int，不然model.fit(X)会报错说无法将float64转化为int64
    for i in range(row):  # 遍历报文，填充矩阵值
        for j in new_packets[i]:
            X[i, j] += 1
    return new_packets, ngram2id, id2ngram, X


# 定义函数，输入相应的参数，并得到模型
# 参数
# 返回值：训练好的模型
def get_model(file_name, n_topics, n_iter, alpha, eta):
    packets = read_inputs(file_name)
    num = len(packets)
    for i in range(num):
        packets[i] = packets[i].split("-")
    # 预处理，得到编号以及训练数据
    new_packets, ngram2id, id2ngram, X = preprocess(packets)
    # 训练模型
    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, alpha=alpha, eta=eta, random_state=1)
    model.fit(X)
    return model
