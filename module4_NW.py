import random


# 全局变量
match_score = 6  # 匹配得分
dismatch_score = -3  # 不匹配得分
gap_score = -2  # 插入空格得分
gap_character = '-'  # 输出时代表插入空格


# 根据两个字符串计算得分矩阵
# 参数：两个字符串s1和s2
# 返回值：得分mat，几层列表的嵌套形式，s1第i个元素，s2第j个元素，对应mat[i][j]
# mat[i][j][0]: 数值，表示该位置最大得分值为多少，
# mat[i][j][1]: 列表，表示该最大得分值来自h_val,d_val,v_val的哪一个或者哪几个，即左方，左上角，上方
def compute_scores(s1, s2):
    # 初始化
    row = len(s1) + 1
    col = len(s2) + 1
    mat = [[[[None] for i in range(2)] for i in range(col)] for i in range(row)]
    # 第0行与第0列
    for i in range(row):
        mat[i][0] = [gap_score*i, []]
    for j in range(col):
        mat[0][j] = [gap_score*j, []]
    # 遍历两个字符串每个对应的位置
    for i in range(1, row):
        for j in range(1, col):
            score = match_score if (s1[i-1] == s2[j-1]) else dismatch_score
            # 三个取值来源，取最大值
            h_val = mat[i][j-1][0] + gap_score
            d_val = mat[i-1][j-1][0] + score
            v_val = mat[i-1][j][0] + gap_score
            o_val = [h_val, d_val, v_val]
            mat[i][j] = [max(o_val), [i+1 for i, v in enumerate(o_val) if v == max(o_val)]]  # h = 1, d = 2, v = 3
    return mat


# 递归函数，在计算好的得分矩阵基础上，逆向寻找某位置最大得分值的路径
# 参数：得分矩阵/嵌套列表mat，当前两个字符串中的位置curr_i, curr_j，当前已有路径path
# 返回值：无，更新的是一个全局列表DIGIT_PATHES
def find_path(mat, curr_i, curr_j,  digit_paths, path=''):
    i = curr_i
    j = curr_j
    # 加上这一句判断，不用找到所有的对齐方式，否则序列教长时递归的复杂度太大
    # 找到最多4个即可结束递归
    if(len(digit_paths) >= 1):
        return
    if i == 0 and j == 0:  # 两边同时结束，用2表示
        digit_paths.append(path)
        return 2
    dir_t = len(mat[i][j][1])  # matrix[i][j][1]表示该位置得分值的来源，可能有多个
    # 若dir_t小于等于1，则只有一个来源，不用考虑多种选择
    while dir_t <= 1:
        n_dir = mat[i][j][1][0] if (i != 0 and j != 0) else (1 if i == 0 else (3 if j == 0 else 0))
        path = path + str(n_dir)
        # 判断走三个方向的哪一个，1为左，2为左上，3为上，并更新当前位置
        if n_dir == 1:
            j = j-1
        elif n_dir == 2:
            i = i-1
            j = j-1
        elif n_dir == 3:
            i = i-1
        # 更新方向取值
        dir_t = len(mat[i][j][1])
        if i == 0 and j == 0:
            digit_paths.append(path)
            return 3
    # 若dir_t大于1，说明有多个方向来源，需要遍历，考虑每一个
    if dir_t > 1:
        for dir_c in range(dir_t):
            n_dir = mat[i][j][1][dir_c] if (i != 0 and j != 0) else (1 if i == 0 else (3 if j == 0 else 0))
            tmp_path = path + str(n_dir)
            if n_dir == 1:
                n_i = i
                n_j = j-1
            elif n_dir == 2:
                n_i = i-1
                n_j = j-1
            elif n_dir == 3:
                n_i = i-1
                n_j = j
            find_path(mat, n_i, n_j, digit_paths, tmp_path)  # 递归调用


# 将数字方向表示的路径转化为原始字符串序列
# 参数：得分矩阵/嵌套列表mat，两个字符串s1和s2，不用输入DIGIT_PATHES，因为定义为global了
# 返回值：字符串对齐后的结果
def path_to_string(mat, s1, s2, digit_paths):
    i = len(s1)  # 初始化矩阵行数 = 序列1长度+1
    j = len(s2)  # 初始化矩阵列数 = 序列2长度+1
    score = mat[i][j][0]  # 右下角得分值，即总分值
    l_i = i
    l_j = j
    answer = []  # 存储输出的序列
    find_path(mat, i, j, digit_paths)  # 调用函数
    # digit_paths 中记录的path是路径方向的数字编号，需要转化为字符串表示，存到answer中
    for elem in digit_paths:
        i = l_i-1
        j = l_j-1
        side_aln = ''
        top_aln = ''
        step = 0
        aln_info = []
        for n_dir_c in range(len(elem)):
            n_dir = elem[n_dir_c]
            score = mat[i+1][j+1][0]
            step = step + 1
            aln_info.append([step, score, n_dir])
            if n_dir == '2':
                side_aln = side_aln + s1[i]
                top_aln = top_aln + s2[j]
                i = i-1
                j = j-1
            elif n_dir == '1':
                side_aln = side_aln + gap_character
                top_aln = top_aln + s2[j]
                j = j-1
            elif n_dir == '3':
                side_aln = side_aln + s1[i]
                top_aln = top_aln + gap_character
                i = i-1
        answer.append([top_aln[::-1], side_aln[::-1]])
    return answer


def same_string(s1, s2):
    matrix = compute_scores(s1, s2)  # 计算得分
    digit_paths = []
    paths = path_to_string(matrix, s1, s2, digit_paths)  # 得到对齐的结果
    align1 = paths[0][0]  # 仅保留第一种对齐方式的两个字符串
    align2 = paths[0][1]
    # 遍历对齐结果，仅保留匹配上的部分
    i = 0
    same = ""
    while(i < len(align1)):
        if(align1[i] == align2[i]):  # 匹配的字符
            same += align1[i]
        # else:
        #    if tmp[-1] != "*":  # 为了间隔开不同的匹配段
        #        tmp += "...*"
        i += 1
    return [align1, align2, same]


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


# 函数：对文件中同一种格式的报文进行多序列对比，得到固定字节组成的字符串
# 参数：文件名
# 返回值：固定字节组成的字符串
def format_string(file_name):
    inputs = read_inputs(file_name)
    num = len(inputs)
    son = num // 5  # 10个报文作为一个子区间
    e = 10  # 阈值，决定保留或者删除两串的对齐结果，用于应对聚类错误的串

    # 多次随机删除，防止聚类有误
    delete_ans = []  # 存放多次随即删除和阈值判断后的结果
    for i in range(4):
        random_inputs = random.sample(inputs, len(inputs)//2)  # 每次随机删除一半，即只保留一半的报文
        random_inputs.sort(key=lambda i: len(i))  # 按长度排序
        # 多次打乱，防止可能出现的匹配不完全
        shuffle_ans = []  # 存放多次随机打乱后的结果
        for j in range(5):
            shuffle_inputs = []
            for k in range(son):  # 将报文在各个小区间内打乱，random.shuffle会改变原有列表，而不是生成新列表
                tmp = random_inputs[k*20:(k+1)*20]
                random.shuffle(tmp)
                shuffle_inputs += tmp
            random_inputs = shuffle_inputs  # 作为下一次的输入，不是总对原始txt进行打乱
            # 初始化
            t = 0  # 记录第几轮遍历了
            raw = shuffle_inputs
            # 多轮遍历，直到只剩下一个格式串
            while len(raw) > 1:
                same = []  # 保存本轮遍历提取的字符串
                num = len(raw)  # raw是本轮遍历的内容
                if(num % 2 != 0):  # 防止奇数，i+1可能越界
                    num -= 1
                for k in range(0, num, 2):  # 遍历raw中串，进一步提取相同格式串
                    res = same_string(raw[k], raw[k+1])
                    if len(res[2]) > e:  # 阈值判断，只保留长度超过阈值的
                        same.append(res[2])
                raw = same  # 下一轮初始化
                t += 1
            if(len(same) != 0):  # 防止最后一轮遍历时由于不满足阈值限制导致结果为空
                shuffle_ans.append(same[0])  # 每次随机过程完全结束后，存储最终得到的格式串
        # 按频数排序，取频数最高的，作为本次随机打乱后的结果
        freq_dict = {}
        for k in shuffle_ans:
            freq_dict[k] = shuffle_ans.count(k)
        ordered = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)  # 按照字典的value排序
        print("\n第%d次随机删除后，多次随机打乱的结果按频率排序为：" % (i+1))
        print(ordered)
        print("频数最高的格式串为：", ordered[0][0])
        # 存储频数最高的格式串，作为最外面循环的一次结果
        delete_ans.append(ordered[0][0])
        print("当前存储的可能格式串为：", delete_ans)
    # 仍是频数最高的作为返回结果
    freq_dict = {}
    for k in delete_ans:
        freq_dict[k] = delete_ans.count(k)
    ordered = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)  # 按照字典的value排序
    return ordered[0][0]  # 返回最长格式串


# 函数：将固定字节组成的连续字符串拆分开，得到报文中对应的多个格式串
# 参数：文件名，字符串列表(只有一个字符串元素)
# 返回值：拆分后得到的字符串列表
def break_string(file_name, same):
    # 读取报文，按照报文长度升序排序
    packets = read_inputs(file_name)
    packets.sort(key=lambda i: len(i))
    sample = random.sample(packets, 4)  # 随机选择4个报文
    e = 10  # 阈值，判定是否选到了错误报文
    res1 = same_string(sample[0], sample[1])
    res2 = same_string(sample[2], sample[3])
    res3 = same_string(res1[2], res2[2])
    if min(len(res1[2]), len(res2[2]), len(res3[2])) > e:  # 认为没有选到错误报文，开始拆分，下面所有代码都在if内
        all_res = []  # 记录与多个报文进行比对后的多个拆分结果
        # 得到根据不同报文得到的可能不同的拆分结果，记录在all_res中
        for i in sample:
            tmp1 = i  # 报文的字符串
            tmp2 = same  # 多序列对比提取的固定格式串
            start = 0
            end = 1
            res = []
            while(end <= len(tmp2)):
                while tmp1.find(tmp2[start:end]) != -1:  # 匹配最长子串
                    end += 1
                    if(end == len(tmp2)+1):  # 最后一个字符属于某子串，防止end无穷加下去
                        break
                end -= 1
                res.append(tmp2[start:end])  # 输出该匹配的子串
                start = end  # 更新位置，为下一轮做准备
                if(end == len(tmp2)):
                    break
            all_res.append(res)
        # 对all_res进行处理，得到最终的拆分结果
        # 首先，得到最大的子串数目，即最细致的，删除字串数目小于n的，因为可能合并了原本分开的子串
        length = []
        for i in range(4):
            length.append(len(all_res[i]))
        n = max(length)  # 子串个数
        m = 4  # 报文数目/all_res中元素个数
        i = 0
        while i < m:
            if len(all_res[i]) < n:
                all_res.pop(i)
                m -= 1
            i += 1
        # 遍历剩下来的可能结果，对于每个子串，删除长度较长对应的拆分结果
        for i in range(n):  # 遍历几个子串
            j = 0
            while j < m-1:  # 遍历根据每个报文的拆分结果，删除长度较长子串对应的拆分
                if len(all_res[j][i]) > len(all_res[j+1][i]):  # 当前较长，删除
                    all_res.pop(j)
                    m -= 1
                elif len(all_res[j][i]) < len(all_res[j+1][i]):  # 下一个较长，删除下一个
                    all_res.pop(j+1)
                    m -= 1
                else:  # 长度相等
                    j += 1
        return all_res


if __name__ == "__main__":
    # cluster1.txt
    # 先多序列对比，得到固定格式串
    print("cluster1.txt")
    print("第一步，进行多序列对比，得到固定格式字符串，提取的过程如下所示")
    same_res = format_string("cluster1.txt")
    print("\n最终得到的格式字符串为：\n", same_res)
    # 拆分格式串
    print("\n第二步，对固定格式字符串进行拆分")
    break_res = break_string("cluster1.txt", same_res)
    print("格式字符串拆分结果为：\n", break_res)

    # cluster2.txt
    # 先多序列对比，得到固定格式串
    print("\n\ncluster2.txt")
    print("第一步，进行多序列对比，得到固定格式字符串，提取的过程如下所示")
    same_res = format_string("cluster2.txt")
    print("最终得到的格式字符串为：\n", same_res)
    # 拆分格式串
    print("\n第二步，对固定格式字符串进行拆分")
    break_res = break_string("cluster2.txt", same_res)
    print("格式字符串拆分结果为：\n", break_res)

    # cluster3.txt
    # 先多序列对比，得到固定格式串
    print("\n\ncluster3.txt")
    print("第一步，进行多序列对比，得到固定格式字符串，提取的过程如下所示")
    same_res = format_string("cluster3.txt")
    print("\n最终得到的格式字符串为：\n", same_res)
    # 拆分格式串
    print("\n第二步，对固定格式字符串进行拆分")
    break_res = break_string("cluster3.txt", same_res)
    print("格式字符串拆分结果为：\n", break_res)

    # cluster4.txt
    # 先多序列对比，得到固定格式串
    print("\n\ncluster4.txt")
    print("第一步，进行多序列对比，得到固定格式字符串，提取的过程如下所示")
    same_res = format_string("cluster4.txt")
    print("\n最终得到的格式字符串为：\n", same_res)
    # 拆分格式串
    print("\n第二步，对固定格式字符串进行拆分")
    break_res = break_string("cluster4.txt", same_res)
    print("格式字符串拆分结果为：\n", break_res)
