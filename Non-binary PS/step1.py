# # txt 转 csv

import numpy as np
import pandas as pd
import os


def each_file(filepath):
    path_dir = os.listdir(filepath)
    count1 = 0
    for allDir in path_dir:
        count1 = count1 + 1
        child1 = os.path.join('%s%s' % (filepath, allDir))
        print(child1)
        txt_dir = os.listdir(child1)
        count2 = 0
        for eachTxt in txt_dir:
            count2 = count2 + 1
            child2 = os.path.join(child1 + "\\" + eachTxt)
            print(child2)
            txt = np.loadtxt(child2)
            txtDF = pd.DataFrame(txt)
            if count1 < 10:
                txtDF.to_csv("G:\\python_demo\\data\\p\\ip0" + str(count1) + "\\ip" + str(count2)
                + ".csv", index=False)
                '''
                txtDF.to_csv("G:\\python_demo\\data\\s\\is0" + str(count1) + "\\is" + str(count2) +
                ".csv", index=False)
              '''
            else:
               txtDF.to_csv("G:\\python_demo\\data\\p\\ip" + str(count1) + "\\ip" + str(count2) + ".csv", index=False)
               #txtDF.to_csv("G:\\python_demo\\data\\s\\is" + str(count1) + "\\is" + str(count2) + ".csv", index=False)


if __name__ == '__main__':  # ok
    filepath = "G:\\KY2\\inp\\"
    filepath = "G:\\KY2\\ins\\"
    each_file(filepath)



