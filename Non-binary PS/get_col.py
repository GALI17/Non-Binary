#获取每个csv文件的列数
import csv


def getCol(inn):
    # 获取每个csv文件的列数
    in_road_2 = inn.replace("\\", "\\\\")
    print(in_road_2)

    #获取列数
    input_csv = csv.reader(open(in_road_2, 'r'))
    col_num = ""
    for col in input_csv:
        col_num = col
    print(len(col_num))
    return len(col_num)


if __name__ == "__main__":  # ok
    getCol("G:\python_demo\data\p\ip01\ip1.csv")
