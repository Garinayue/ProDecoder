import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import module2_lda


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


# 定义函数，训练lda模型并使用其结果对原始文件聚类，结果存到不同的文件中
# 参数：除了模型 参数，还加了一个n_cluster，簇的最大个数
def get_clusters(file_name, n_topics, n_iter, alpha, eta, n_cluster):
    model = module2_lda.get_model(file_name, n_topics, n_iter, alpha, eta)
    message_topic = model.doc_topic_
    # 层次聚类，且是自底向上的凝聚聚类
    X = message_topic  # 输入数据，lda模型得到的矩阵
    disMat = sch.distance.pdist(X, 'euclidean')  # 生成点与点之间的距离矩阵,使用欧氏距离
    Z = sch.linkage(disMat, method='average')  # 层次聚类编码为一个linkage矩阵
    # 画图
    P = sch.dendrogram(Z)
    plt.title('Dendrogram')
    plt.xlabel('Messages')
    plt.ylabel('Euclidean distances')
    plt.show()
    cluster = sch.fcluster(Z, t=n_cluster, criterion='maxclust')  # 指定簇的个数最大为4
    print("\n聚类结果为：\n", cluster)
    # 根据聚类结果，将报文按照所属的簇存到不同的文件中
    packets = module2_lda.read_inputs("inputs.txt")  # 读取原始报文
    num = len(packets)
    n = n_cluster
    for i in range(n):  # 针对不同的簇
        cluster_packets = []  # 记录属于该簇的报文
        for j in range(num):  # 遍历每个报文，看属于哪个簇
            if cluster[j] == i+1:  # 簇是从1开始编号的
                cluster_packets.append(packets[j])
        file_name = "cluster" + str(i+1) + ".txt"
        save_file(file_name, cluster_packets)  # 每个簇存到对应的文件中


if __name__ == "__main__":
    get_clusters("freq_ngrams.txt", 4, 500, 0.5, 0.005, 4)
