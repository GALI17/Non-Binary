# # txt 转 csv

import numpy as np
import pandas as pd

txt = np.loadtxt("C:\\Users\\Administrator\\Desktop\\123\\p32-30")
txtdf = pd.DataFrame(txt)
txtdf.to_csv("C:\\Users\\Administrator\\Desktop\\123\\p32-30.csv", index=False)


