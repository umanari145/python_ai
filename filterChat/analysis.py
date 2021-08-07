import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        for userId in ["112", "272", "52", "512", "832"]:
            plt.figure()
            plt.xlabel('month')
            plt.ylabel('revenue')

            sql = "select target_month, SUM(dmm_point + no_dmm_point + other_point) as total_point from rewards where is_delete = 0 and user_id = %s group by target_month" % (userId)
            memberRewards = self._db.select(sql)
            df = pd.DataFrame.from_records(memberRewards)
            df = df.dropna()
            
            model_lr = LinearRegression()
            #to_numpy().reshape(-1,1)は次元の調整
            model_lr.fit(df.index.to_numpy().reshape(-1, 1), df.total_point.to_numpy().reshape(-1, 1))

            plt.plot(df.index, df.total_point, label = userId)
            plt.plot(df.index, model_lr.predict(df.index.to_numpy().reshape(-1, 1)), linestyle="solid")

            plt.legend()
            filePath = "images/img_%s" % (userId)
            plt.savefig(filePath)

