import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from itertools import groupby
class analysis:

    def __init__(self, db):
        self._db = db

    def rewardsCheck(self):

        plt.figure()
        totalRewards = self._db.select("select target_month, SUM(dmm_point + no_dmm_point + other_point) as total_point from rewards where is_delete = 0 group by target_month" )

        df = pd.DataFrame.from_records(totalRewards)
        #欠損値の削除
        df = df.dropna()

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        model_lr = LinearRegression()
        #to_numpy().reshape(-1,1)は次元の調整
        model_lr.fit(df.index.to_numpy().reshape(-1, 1), df.total_point.to_numpy().reshape(-1, 1))

        plt.xlabel('month')
        plt.ylabel('revenue')
        plt.plot(df.index, df.total_point, label = "total revenue")
        plt.plot(df.index, model_lr.predict(df.index.to_numpy().reshape(-1, 1)), linestyle="solid")
        plt.legend()
        plt.savefig('images/all_img.png')

    def memberCheck(self):

        for userId in ["112", "272", "52", "512", "832"]:
            plt.figure()
            plt.xlabel('month')
            plt.ylabel('revenue')

            sql = "select target_month, SUM(dmm_point + no_dmm_point + other_point) as total_point from rewards where is_delete = 0 and user_id = %s group by target_month" % (userId)
            memberRewards = self._db.select(sql)
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
            filePath = "images/img_%s" % (userId)
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
        df = df[df.groupby(["target_month"])["percent"].rank(ascending = False) <=2]

        #月でグルーピングしてパーセントして合計値をだす
        df = df.groupby(["target_month"])["percent"].sum()

        plt.plot(df.to_numpy())

        plt.legend()
        filePath = "images/img_oligopoly"
        plt.savefig(filePath)