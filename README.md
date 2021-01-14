# ProDecoder

尝试简单复现ProDecoder协议逆向方法

### 环境

lda库



## 实验过程

可以删除几个txt文件，然后按序运行module0_inputs.py、module1_ngrams.py、module3_sch.py和module4_NW.py，跳过module2_lda.py(无需运行)。在运行module0_inputs.py时，需要运行四次，每次改变注释掉的固定格式内容，即依次产生四种格式的报文。

或者也可以保留inputs.txt文件，便无需运行module0_inputs.py。



### module0_inputs.py

自己设计一种简单的报文格式，并批量得到报文，共设计了4中不同的报文格式，4种报文的区别主要在于固定格式字段的内容。

1. 第一种："68656164"固定开头 + “6672”固定内容 + 4个字节随机内容 + "746f"固定内容 + 4个字节随机内容 + “ffff”固定内容 + 布尔值"00"或"01" + 一字节随机数(指示后面的半字节长度) + 随机内容
2. 第二种："12345678"固定开头 + “3344”固定内容 + 4个字节随机内容 + "8899"固定内容 + 4个字节随机内容 + “ffff”固定内容 + 布尔值"00"或"01" + 一字节随机数(指示后面的半字节长度) + 随机内容
3. 第三种："19991023"固定开头 + “0915”固定内容 + 4个字节随机内容 + "0614"固定内容 + 4个字节随机内容 + “ffff”固定内容 + 布尔值"00"或"01" + 一字节随机数(指示后面的半字节长度) + 随机内容
4. 第四种："56785678"固定开头 + “2020”固定内容 + 4个字节随机内容 + "1226"固定内容 + 4个字节随机内容 + “ffff”固定内容 + 布尔值"00"或"01" + 一字节随机数(指示后面的半字节长度) + 随机内容  

按照以上四种格式，依次各生成100条报文，存储在文件 inputs.txt 中



### module1_ngrams.py

输入：读取 inputs.txt 文件中的400条报文

大致过程：

1. 提取所有报文中的n-grams并统计各自的频率，降序排序
2. 保留频率和小于等于P的n-grams，其余的删除
3. 遍历每条报文的n-grams列表，只保留在高频n-grams列表中出现的

输出：freq_ngrams.txt 文件，共400条记录，每条记录对应报文删减后的n-grams，用 - 隔开



### module2_lda.py

使用自然语言中的基于Gibbs采样的LDA模型，n-gram对应模型的词语，报文对应模型的文档，关键词对应模型的主题。

组织训练数据X：矩阵，行数=报文数目，列数=不同的n-grams数目，第i行第j列元素代表第i个报文中第j个n-grams出现了几次

模型参数：n_topics(主题数目)，n_iter(训练的迭代次数)，alpha和eta(Gibbs采样的参数)



### module3_sch.py

使用LDA模型的训练结果进行聚类，每个报文的特征为其在n个关键词的概率分布

采用的聚类方式为层次聚类，聚类结果中，每一个簇的报文存储到一个单独的txt文件中，分别对应到cluster1.txt, cluster2.txt, cluster3.txt, cluster4.txt



### module4_NW.py

多序列对比，提取每一种报文的固定格式字段

使用Needleman Wunsch算法进行两个序列间的对比，设置相应的得分值，合并对齐相同的字段为一个字符串。为了进行多个序列的对比

1. 将报文按照长度递增排序
2. 多次迭代，每次对相邻两个报文调用NW算法，直到只剩下一个字符串，即为相同格式串合并的串
3. 拆分格式串：为了防止偶然性，随机选择五条报文，用格式串与其匹配拆分，保留匹配子字段较短的



### 待改进的方向

前两个问题比较主要，关于容忍噪声以及鲁棒性方面

1. 聚类过程中若有报文聚类错误，一个聚类错误的报文可能会导致对齐结果完全错误
2. 聚类完全正确的情况下，两个聚类正确的报文对齐错误也可能导致错误一直延续，使最终结果完全不对
3. 是否支持更长长度的报文
4. 时间复杂度是否可以改进
