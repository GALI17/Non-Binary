import os
import get_col
import time
from collections import Counter
import lightgbm as lgb
import numpy as np
import pandas as pd
from numpy import loadtxt
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, precision_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import datetime


top_num = 30
#data_dimension = 12  # 一共有几列

csv_file = []
real_file = []

csv = "G:\\python_demo\\data\\s\\"
real = "G:\\python_demo\\res\\res_s\\"

road = [csv, real]
file = [csv_file, real_file]


def read_path(road_path, file_path):  # ok
    for i in range(len(road_path)):
        path(road_path[i], file_path[i])


def path(save_road, save_file):  # ok
    path_dir = os.listdir(save_road)
    for eachDir in path_dir:
        child1 = os.path.join('%s%s' % (save_road, eachDir))
        print(child1)
        txt_dir = os.listdir(child1)
        for eachTxt in txt_dir:
            child2 = os.path.join(child1 + "\\" + eachTxt)
            print(child2)
            save_file.append(child2)


def each_file(all_csv, all_real):  # ok
    for i in range(len(all_csv)):
        single_real_count = []  # 存储1个小类得到的全部索引
        print(all_csv[i])
        # 挖掘得到 top_index
        top_index = fun(all_csv[i])
        print(top_index)
        for j in range(len(top_index)):
            single_real_count.append(top_index[j][0])
        read_update_out(all_real[i], single_real_count)


#读real进来，依据本次的single_real_count更新real，然后输出new_real即可
def read_update_out(each_real, real_count):
    real_tempt = loadtxt(each_real, delimiter=" ")
    print(real_tempt)
    out_real = []  # 新的real
    for i in range(len(real_count)):
        top_col = real_count[i]
        out_real.append(real_tempt[top_col])
    # 输出最后选定的排名前10的索引号
    print(out_real)
    np.set_printoptions(suppress=True)
    np.savetxt(each_real, out_real, fmt='%d', delimiter=' ')


#执行函数,得到top_index
def fun(in_road):  # ok
    start = time.time()
    index = []
    # 获取csv文件里面一共有几列
    col_num = get_col.getCol(in_road)
    data_dimension = col_num-1

    # 载入数据集
    dataset = loadtxt(in_road, delimiter=",", skiprows=1)
    print(type(dataset))

    # split data into x and y
    x = dataset[:, 0:data_dimension]  # x[:,m:n]，即取所有数据的第m到n-1列数据，含左不含右
    y = dataset[:, data_dimension]

    random_s = [8, 20, 40, 100, 200, 1000]  # 依据不同的种子运算多次，之后进行投票选择继续约减
    for rs in random_s:
        # 把数据集拆分成训练集和测试集
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=rs)

        print("-----------------XGBoost-----------------")

        # 拟合XGBoost模型
        model1 = XGBClassifier(learning_rate=0.1,
                               n_estimators=1000,  # 树的个数--1000棵树建立xgboost
                               max_depth=5,  # 树的深度
                               min_child_weight=1,  # 叶子节点最小权重
                               gamma=0.,  # 惩罚项中叶子结点个数前的参数
                               subsample=0.8,  # 随机选择80%样本建立决策树
                               colsample_btree=0.8,  # 随机选择80%特征建立决策树
                               objective='reg:logistic',  # 指定损失函数
                               scale_pos_weight=1,  # 解决样本个数不平衡的问题
                               random_state=27  # 随机数种子
                               )
        model1.fit(x_train, y_train)

        # 强特征排序
        importance = model1.feature_importances_
        top = pd.Series(importance).sort_values(ascending=False)

        # 输出前10的index索引
        print(list(top.index)[:top_num])
        index.extend(list(top.index)[:top_num])

        # 对测试集做预测
        y_pred = model1.predict(x_test)
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))
        precision = precision_score(y_test, predictions)
        print("precision: %.2f%%" % (precision * 100.0))

        print("-----------------LightGBM-----------------")

        params = {
            'task': 'train',
            'boosting_type': 'gbdt',  # GBDT算法为基础
            'objective': 'binary',
            'metric': 'auc',  # 评判指标
            'max_bin': 255,  # 大会有更准的效果,更慢的速度
            'learning_rate': 0.1,  # 学习率
            'num_leaves': 64,  # 大会更准,但可能过拟合
            # 'max_depth': -1,   小数据集下限制最大深度可防止过拟合,小于0表示无限制
            'feature_fraction': 0.8,  # 防止过拟合
            'bagging_freq': 5,  # 防止过拟合
            'bagging_fraction': 0.8,  # 防止过拟合
            'min_data_in_leaf': 10,  # 防止过拟合
            'min_sum_hessian_in_leaf': 3.0,  # 防止过拟合
            # 'header': True   数据集是否带表头
            'verbose': -1  # 忽略掉警告：No further splits with positive gain, best gain: -inf
        }

        lgb_train = lgb.Dataset(x_train, label=y_train)
        model2 = lgb.train(params, train_set=lgb_train)

        importance = model2.feature_importance()
        top = pd.Series(importance).sort_values(ascending=False)
        print(list(top.index)[:top_num])
        index.extend(list(top.index)[:top_num])

        y_pred = model2.predict(x_test)
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))
        precision = precision_score(y_test, predictions)
        print("precision: %.2f%%" % (precision * 100.0))

        print("-----------------ExtraTree是随机森林的一个变种-----------------")

        model4 = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
        model4.fit(x_train, y_train)

        importance = model4.feature_importances_
        top = pd.Series(importance).sort_values(ascending=False)
        print(list(top.index)[:top_num])
        index.extend(list(top.index)[:top_num])

        y_pred = model4.predict(x_test)
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))
        precision = precision_score(y_test, predictions)
        print("precision: %.2f%%" % (precision * 100.0))

    end = time.time()
    running_time = end - start
    print('-----------time--------')
    print(running_time)

    print(index)

    #排序
    sort = get_count_by_counter(index)
    top_index = sort.most_common(top_num)

    return top_index


# 使用collections.Counter()函数
# 直接collections.Counter(list)就可以得到list中每个元素的个数
def get_count_by_counter(ix):  # ok
    count = Counter(ix)  # 类型： <class 'collections.Counter'>
    return count


if __name__ == "__main__":  # ok

    start = datetime.datetime.now()
    #读进来csv数据并挖掘
    read_path(road, file)
    #更新real
    each_file(csv_file, real_file)

    end = datetime.datetime.now()

    print(end-start)












