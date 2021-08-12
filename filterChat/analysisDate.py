import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from sklearn.linear_model import LinearRegression
from itertools import groupby

class analysisDate:

    def __init__(self, db):
        self._db = db

    def rewardsCheck(self):

        totalRewards = self._db.select("select target_month, SUM(dmm_point + no_dmm_point + other_point) as total_point from rewards where is_delete = 0 group by target_month" )

        for eachReward in totalRewards:
            eachReward['target_month'] = str(eachReward['target_month'])[:4] + "-" + str(eachReward['target_month'])[4:7] + "-01"

        df = pd.DataFrame.from_records(totalRewards)
        #欠損値の削除
        df = df.dropna()

        #pd.set_option('display.max_rows', None)
        #pd.set_option('display.max_columns', None)

        #日付型にしないとplot時に文字列判例してしまう
        df["target_month"] = pd.to_datetime(df["target_month"])
        #計算に使いたい場合は数字系もしっかりint変換しておく
        df["total_point"] = df["total_point"].astype(int)

        fig, ax = plt.subplots()
        ax.plot(df["target_month"], df.total_point)

        #X軸について
        #日付出力方式を検討
        daysFmt = mdates.DateFormatter('%Y-%m')
        ax.xaxis.set_major_formatter(daysFmt)
        #いい感じにラベルを回転させてくれる
        fig.autofmt_xdate()
        #ちなみに具体的な回転率を指定したい時
        #plt.xticks(rotation=90)
        #y軸について
        #上限、下限を意識的にとりたい時　0 〜　最大値の1.2倍
        ax.set_ylim(0, df.total_point.max()*1.2)
        #縦軸で〜100万P
        ax.yaxis.set_major_formatter(FuncFormatter(self.major_formatter))
        plt.savefig('images/all_img_date.png')

    def major_formatter(self, x, pos):
        unit = int(x/10000)
        return str(unit) + "MP"
