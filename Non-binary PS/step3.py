import os
import numpy as np

input_file = []
real_file = []

inputData = "G:\\KY2\\p\\"
realData = "G:\\python_demo\\res\\res_p\\"

all_real = []


def read_1(inp):  # ok
    path_dir = os.listdir(inp)
    for allDir in path_dir:
        child1 = os.path.join('%s%s' % (inp, allDir))
        print(child1)
        input_file.append(child1)


def read_2(real):  # ok
    path_dir = os.listdir(real)
    for allDir in path_dir:
        child1 = os.path.join('%s%s' % (real, allDir))
        #print(child1)
        txt_dir = os.listdir(child1)
        for eachTxt in txt_dir:
            child2 = os.path.join(child1 + "\\" + eachTxt)
            print(child2)
            real_file.append(child2)


def add_update_real(real):  # ok
    add = []
    for i in range(len(real)):
        print("i :")
        print(i)
        real_tempt = np.loadtxt(real[i], delimiter=' ')  # <class 'numpy.ndarray'>
        print(real_tempt)
        if (i+1) % 3 != 0:
            add.extend(real_tempt)  # <class 'list'>
            print("if add:")
            print(add)
        else:
            add.extend(real_tempt)
            del_repeat = list(set(add))
            np.set_printoptions(suppress=True)
            out = np.transpose(del_repeat)
            print("out: ")
            print(out)

            all_real.append(out)
            add = []
            print("else add:")
            print(add)

            print(i)
            print(real[i])
            print(i-1)
            print(real[i-1])
            print(i-2)
            print(real[i-2])

            np.savetxt(real[i - 2], out, fmt="%d", delimiter=' ')
            np.savetxt(real[i - 1], out, fmt="%d", delimiter=' ')
            np.savetxt(real[i], out, fmt="%d", delimiter=' ')


def update_each_input(inp, all_real):  # ok
    for i in range(len(inp)):
        real_tempt = all_real[i]
        print(real_tempt)
        out_list = []
        for j in range(len(real_tempt)):
            tempt = int(real_tempt[j])
            print(tempt)
            #S
            #x = np.loadtxt(inp[i], dtype=int, delimiter=" ", usecols=tempt,)
            #P
            x = np.loadtxt(inp[i], delimiter=" ", usecols=tempt, )
            out_list.append(x)

        print(out_list)

        np.set_printoptions(suppress=True)
        out = np.transpose(out_list)
        np.savetxt(inp[i], out, fmt="%s", delimiter=" ")


if __name__ == "__main__":
    #约减实现
    read_1(inputData)
    read_2(realData)
    print(input_file)
    print(real_file)
    #更新real
    add_update_real(real_file)
    #更新聚类前的原始数据
    print(all_real)
    update_each_input(input_file, all_real)












