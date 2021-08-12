import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from sklearn.linear_model import LinearRegression
import io
import pandas as pd


data = """x,y
152,57
173,78
172,83
178,58
166,63
175,66
158,66
163,74
157,64
165,68
176,68
165,60
147,63
153,63
146,47
156,49
145,59
181,66
160,74
140,55
152,55
165,56
170,65
159,51
151,52
167,51
177,82
155,63
159,45
170,66
154,56
163,60
161,70
165,70
150,57
158,53
163,67
186,69
168,68
170,74
155,60
159,49
170,87
163,50
166,58
161,69
159,60
171,71"""

df = pd.read_csv(io.StringIO(data), parse_dates=[0])

#ここで揃えないと回帰直線がうまくいかない
df.sort_values(by="x", inplace=True)

#----通常のplot------
x = df.x
y = df.y
#ValueError: Expected 2D array, got 1D array instead:
#2次元配列が必要なところ、1次元配列を与えているためreshape
plt.plot(x, y, 'o')

#-----学習-------
model = LinearRegression()
model.fit(x.values.reshape(-1, 1), y.values.reshape(-1, 1))

#-----学習したプロット-------
plt.plot(x, model.predict(x.values.reshape(-1, 1)), linestyle='solid')

plt.savefig('images/height_weight.png')
