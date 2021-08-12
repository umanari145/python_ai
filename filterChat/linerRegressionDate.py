import statsmodels.api as sm
import pandas as pd
import numpy as np
import requests
import io
import os
from dotenv import load_dotenv
from matplotlib import pylab as plt
from matplotlib.pylab import rcParams
from sklearn.linear_model import LinearRegression


#参考URL
#https://qiita.com/hcpmiyuki/items/b1783956dee20c6d4700

rcParams['figure.figsize'] = 15, 6

load_dotenv()

URL  = os.environ['DATA_URL']
r = requests.get(URL)
row_data = pd.read_csv(io.BytesIO(r.content))

# float型にしないとモデルを推定する際にエラーがでる
row_data.earnings = row_data.earnings.astype('float64')
row_data.temperature = row_data.temperature.astype('float64')
# datetime型にしてインデックスにする
row_data.date = pd.to_datetime(row_data.date)
data = row_data.set_index("date")
plt.plot(data.temperature)

plt.savefig('images/templature.png')