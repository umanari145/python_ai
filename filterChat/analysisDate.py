import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from itertools import groupby

class analysisDate:

    def __init__(self, db):
        self._db = db

    def sample(self):
        data = """date,value
        2018-12-01 00,15
        2018-12-01 01,30
        2018-12-01 02,25
        2018-12-01 03,18
        2018-12-01 04,9
        2018-12-01 05,22
        2018-12-01 06,34
        2018-12-01 07,33
        2018-12-01 08,28
        2018-12-01 09,22
        2018-12-01 10,26
        2018-12-01 11,31"""
        df = pd.read_csv(io.StringIO(data), parse_dates=[0])

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(df['date'], df['value'])

        ##以下をカスタマイズする
        daysFmt = mdates.DateFormatter('%m/%d %H:%M')
        ax.xaxis.set_major_formatter(daysFmt)
        fig.autofmt_xdate()
        plt.savefig('images/samepl_img.png')

    def rewardsCheck(self):

        totalRewards = self._db.select("select target_month, SUM(dmm_point + no_dmm_point + other_point) as total_point from rewards where is_delete = 0 group by target_month" )

        for eachReward in totalRewards:
            eachReward['target_month'] = str(eachReward['target_month'])[:4] + "-" + str(eachReward['target_month'])[4:7] + "-01"

        df = pd.DataFrame.from_records(totalRewards)
        #欠損値の削除
        df = df.dropna()

        #pd.set_option('display.max_rows', None)
        #pd.set_option('display.max_columns', None)

        #model_lr = LinearRegression()
        #to_numpy().reshape(-1,1)は次元の調整
        #model_lr.fit(df.index.to_numpy().reshape(-1, 1), df.total_point.to_numpy().reshape(-1, 1))

        plt.xlabel('month')
        plt.ylabel('revenue')

        #日付型にしないとplot時に文字列判例してしまう
        df["target_month"] = pd.to_datetime(df["target_month"])
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        ax.plot(df["target_month"], df.total_point)

        #日付出力方式を検討
        daysFmt = mdates.DateFormatter('%Y-%m')
        ax.xaxis.set_major_formatter(daysFmt)
        #いい感じにラベルを回転させてくれる
        fig.autofmt_xdate()
        
        #ちなみに具体的な回転率を指定したい時
        #plt.xticks(rotation=90)

        #plt.plot(df.index, df.total_point, label = "total revenue")
        #plt.plot(df.index, model_lr.predict(df.index.to_numpy().reshape(-1, 1)), linestyle="solid")
        #plt.legend()

        plt.savefig('images/all_img.png')

    def memberCheck(self):

        for userId in ["112", "272", "52", "512", "832"]:
            fig = plt.figure()
            plt.xlabel('month')
            plt.ylabel('revenue')

            sql = "select u.japanese_name, r.target_month, SUM(r.dmm_point + r.no_dmm_point + r.other_point) as total_point from rewards r left join  users u on r.user_id = u.id where r.is_delete = 0 and r.user_id = %s group by r.target_month" % (userId)
            memberRewards = self._db.select(sql)
            for eachmemeber in memberRewards:
                eachmemeber['target_month'] = str(eachmemeber['target_month'])[2:4] + "/" + str(eachmemeber['target_month'])[4:7]

            name = memberRewards[0]['japanese_name']
            df = pd.DataFrame.from_records(memberRewards)
            df = df.dropna()
            #一定数以下の行を削除
            row_to_zero = df.index[df.total_point <= 1000]
            df = df.drop(row_to_zero)

            model_lr = LinearRegression()
            #to_numpy().reshape(-1,1)は次元の調整
            model_lr.fit(df.index.to_numpy().reshape(-1, 1), df.total_point.to_numpy().reshape(-1, 1))

            plt.plot(df.index, df.total_point, label = userId)
            plt.plot(df.index, model_lr.predict(df.index.to_numpy().reshape(-1, 1)), linestyle="solid")

            plt.legend()
            filePath = "images/img_%s" % (name)
            plt.savefig(filePath)


    def oligopoly(self):
        plt.figure()
        plt.xlabel('month')
        plt.ylabel('percent')

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        #ヒアドキュメント
        sql = """
select
	target_month,
	u.id as userId,
	u.`japanese_name`,
	(r.dmm_point + r.no_dmm_point + r.other_point) as total_point,
	(r.dmm_point + r.no_dmm_point + r.other_point) / (select sum(dmm_point + no_dmm_point + other_point) from rewards r2 where r2.is_delete = 0 and r2.target_month = r.target_month) * 100 as percent
from rewards r
	left join users u on r.user_id = u.id
	where r.is_delete = 0
"""
        rewardsAnalysis = self._db.select(sql)
        df = pd.DataFrame.from_records(rewardsAnalysis)
        df = df.dropna()
        row_to_zero = df.index[df.total_point <= 0]
        df = df.drop(row_to_zero)
        #グルーピングを含めた多段ソート(月別、上位メンバー))
        df = df.sort_values(by = ["target_month", "percent"], ascending=[True, False])
        #月ごとの上位３人
        #print(df)
        df = df[df.groupby(["target_month"])["percent"].rank(ascending = False) <= 3]

        #月でグルーピングしてパーセントして合計値をだす
        df = df.groupby(["target_month"])["percent"].sum()
        model_lr = LinearRegression()
        #to_numpy().reshape(-1,1)は次元の調整

        plt.plot(df.to_numpy())
        plt.legend()
        filePath = "images/img_oligopoly"
        plt.savefig(filePath)