import pandas as pd
import matplotlib.pyplot as plt

class analysis:



    def __init__(self, db):
        self._db = db


    def rewardsCheck(self):

        plt.figure()
        totalRewards = self._db.select("select target_month, SUM(dmm_point + no_dmm_point + other_point) as total_point from rewards where is_delete = 0 group by target_month" )
        df = pd.DataFrame.from_records(totalRewards)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
    
        #print(df)
        plt.xlabel('month')
        plt.ylabel('revenue')
        plt.plot(df.index, df.total_point, label = "total revenue")
        plt.legend()
        plt.savefig('img.png')

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
            plt.plot(df.index, df.total_point, label = userId)
            plt.legend()
            filePath = "img_%s" % (userId)
            plt.savefig(filePath)

