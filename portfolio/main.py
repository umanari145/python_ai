import pandas as pd
import numpy as np
import os
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rcParams
import seaborn as sns
from sklearn.linear_model import LinearRegression as LR # 線形回帰のモデル
from sklearn.metrics import mean_squared_error as MSE #評価関数　MSE

class main:

    def __init__(self):

        self.INPUT_DATA_PATH = './sales_data/'

        #訓練用データ
        self.SALES_TRAIN_DATA_FILE = self.INPUT_DATA_PATH + "sales_train.csv"
        # 評価用データ
        self.SALES_TEST_DATA_FILE = self.INPUT_DATA_PATH + "sales_test.csv"
        # 商品マスタデータ
        self.PRODUCT_DATA_FILE= self.INPUT_DATA_PATH + "product_master.csv"
        # カレンダーデータ
        self.CALENDAR_DATA_FILE= self.INPUT_DATA_PATH + "calendar_weather.csv"

        self.sales_train_data = pd.read_csv(self.SALES_TRAIN_DATA_FILE)
        self.sales_test_data = pd.read_csv(self.SALES_TEST_DATA_FILE)
        self.product_data = pd.read_csv(self.PRODUCT_DATA_FILE)
        self.calendar_data = pd.read_csv(self.CALENDAR_DATA_FILE)

        #print(calendar_data)
        #print(sales_test_data)
    def dataProcessing(self):
        sales_train_data = self.sales_train_data
        sales_test_data = self.sales_test_data
        sales_train_data["data_flag"] = 1
        sales_test_data["data_flag"] = 0

        all_sales_data = pd.concat([sales_train_data, sales_test_data],sort=True).reset_index(drop=True)
        all_sales_data = self.mergeData(all_sales_data)
        all_sales_data = self.processMissingValue(all_sales_data)
        
        return all_sales_data

    def mergeData(self, sales_data):
        #テーブル同様 left join
        product_sales_data = pd.merge(sales_data, self.product_data, on="商品コード", how="left")
        #日付ごとに売上をサマるindexを初期化する
        #product_sales_data_byday = product_sales_data.groupby("日付").sum()["売上"].reset_index()
        #total_sales_calendar_data = pd.merge(self.calendar_data, product_sales_data_byday, on = "日付")
        #print(total_sales_calendar_data)
        product_sales_data["月"] = product_sales_data["日付"].apply(lambda x : int(x.split("-")[1]))
        #日付データと商品コードのマージ
        product_sales_calendar_data = pd.merge(self.calendar_data, product_sales_data, on="日付", how="left")

        #トータル売上
        return product_sales_calendar_data

    def processMissingValue(self, calendar_data):
        #欠損値の調査
        #print(calendar_data.isnull().sum())
        #print(calendar_data.isnull().sum() / len(calendar_data) * 100)
        #列指定で削除

        #pd.set_option('display.max_rows', None)
        #pd.set_option('display.max_columns', None)

        #長いので短くする
        calendar_data["天気"] = calendar_data["天気概況(夜：18時～翌日06時)"]

        #これでカテゴリデータをフラグ化できる
        calendar_data = pd.get_dummies(calendar_data, columns=["天気"])
        calendar_data = pd.get_dummies(calendar_data, columns=["月"])
        calendar_data = pd.get_dummies(calendar_data, columns=["曜日"])
        calendar_data.drop("最大風速(風向)", axis=1, inplace=True);
        #平均気温がnullに対して下記のように計算(filter+map)
        calendar_data.loc[calendar_data["平均気温(℃)"].isnull(), "平均気温(℃)"] = (calendar_data["最高気温(℃)"] + calendar_data["最低気温(℃)"]) / 2 
        #販売個数がnullの場合,drop(モデル作成時のみ)
        #calendar_data.dropna(subset=["販売個数"], inplace=True)

        return calendar_data
    
    def makeModel(self, calendar_data):
        
        product_name_arr = set(calendar_data["商品名"])
        for product_name in product_name_arr:
            train_data = calendar_data[(calendar_data["商品名"] == product_name ) & (calendar_data["data_flag"] == 1)]
            test_data = calendar_data[(calendar_data["商品名"] == product_name ) & (calendar_data["data_flag"] == 0)]

            if ((product_name is np.nan) == False & len(train_data) >= 0 & len(test_data) >= 0):
                self.predictSales(product_name, train_data, test_data)


    def dropOutlier(self, calendar_data):
        q3 = calendar_data["販売個数"].quantile(0.75)
        q1 = calendar_data["販売個数"].quantile(0.25)
        iqr = q3 - q1

        bottom_value = q1 - (1.5 * iqr)
        top_value = q3 + (1.5 * iqr)
        calendar_data = calendar_data[(calendar_data["販売個数"]>=bottom_value ) & (calendar_data["販売個数"]<=top_value)]
        return calendar_data

    def predictSales(self, product_name, train_data, test_data):

        if (product_name == "ワイン"):
            #case1
            val_columns = ["曜日_金", "曜日_土", "曜日_日", "平均気温(℃)", "月_7.0"]
            #case2
            val_columns = ["曜日_金", "曜日_土", "曜日_日", "平均気温(℃)", "月_7.0", "休日", "天気_晴", "天気_曇", "天気_雨"]
            #case3
            val_columns = ["休日", "平均気温(℃)", "月_7.0"]
        else:
            #case1
            val_columns = ["曜日_金", "曜日_土", "曜日_日", "平均気温(℃)"]
            #case2
            val_columns = ["曜日_金", "曜日_土", "曜日_日", "平均気温(℃)", "休日", "天気_晴", "天気_曇", "天気_雨"]
            #case3
            val_columns = ["休日", "平均気温(℃)"]

        #pd.set_option('display.max_columns', None)
        x_train = train_data[val_columns]
        # テストデータに入っている正解値
        y_train = train_data["販売個数"]

        #self.monthlyPlot(train_data, product_name)

        linear = LR()
        linear.fit(x_train, y_train)

        x_test = test_data[val_columns]
        # テストデータに入っている正解値
        y_test = test_data["販売個数"]
        pred = linear.predict(x_test)
        #日付と解答と予測値のマージとすり合わせ
        p = pd.DataFrame({"正解値":y_test,"予測値":pred,"日付":test_data["日付"]})
        plt.rcParams['figure.figsize'] = (20.0, 20.0)
        p.plot(x="日付", figsize=(15,4))
        filePath = 'images/product_trend/case_three/product_%s_predict.png' % product_name
        plt.savefig(filePath)
        print("商品名", product_name ,"RMSE",np.sqrt(MSE(y_test,pred)))


    def plotting(self, calendar_data):
        #月ごとの商品ごとの販売数
        #self.calcRevenue(calendar_data)
        productNameArr = set(calendar_data["商品名"].values)
        for productName in productNameArr:
            #self.productCountByProduct(calendar_data, productName)
            self.scatterGraph(calendar_data, productName)
            self.saveProductImage(calendar_data, productName)
            #self.montlyReport(calendar_data, productName)


    # 商品ごとの販売数、平均値、中央値を出力
    def productCountByProduct(self, calendar_data, product_name):
        product_sale = calendar_data[calendar_data["商品名"] == product_name]
        if (len(product_sale) == 0):
            return None

        #商品ごとの販売個数の分析値
        print("商品名:", product_name)
        print("平均値:", product_sale["販売個数"].mean())
        print("中央値:", product_sale["販売個数"].median())


    #売上の出力
    def calcRevenue(self, calendar_data):

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        
        calendar_data["年"] = calendar_data["日付"].apply(lambda x : int(x.split("-")[0]))
        calendar_data = calendar_data[calendar_data["年"] == 2018]

        calendar_data["売上"] = calendar_data["販売個数"] * calendar_data["価格"]
        calendar_data = calendar_data.groupby(["月", "商品名"]).sum()["売上"].reset_index()
        month_arr = set(calendar_data["月"])
        month_sale_arr = []
        for month in month_arr:
            montlyRevenu = calendar_data[calendar_data["月"] == month].sum()["売上"]
            #抽出した列(特定月)への挿入
            calendar_data.loc[calendar_data["月"] == month, ["月総売上"]] = montlyRevenu
            month_sale_arr.append(montlyRevenu)
        calendar_data["%"] = calendar_data["売上"] / calendar_data["月総売上"] * 100
        calendar_data = calendar_data.sort_values(by = ["月", "売上"], ascending=[True, False])

        product_arr = set(calendar_data["商品名"])

        for product_name in product_arr:
            print("商品ごとの月平均売上:", product_name, calendar_data[calendar_data["商品名"] == product_name]["売上"].mean())

        print("月別、商品別売上")
        print(calendar_data)

    def monthlyPlot(self, calendar_data, product_name):

        calendar_data["年"] = calendar_data["日付"].apply(lambda x : int(x.split("-")[0]))
        calendar_data = calendar_data[calendar_data["年"] == 2018]

        product_sale = calendar_data[(calendar_data["商品名"] == product_name)]
        if (len(product_sale) == 0):
            return None
        plt.rcParams['figure.figsize'] = (60.0, 20.0)
        p = pd.DataFrame({"日付":calendar_data["日付"], "販売個数":calendar_data["販売個数"]})
        p.plot(x="日付", figsize=(55,4))
        filePath = 'images/product_trend/regular/product_%s_predict.png' % product_name
        plt.savefig(filePath)
        

    #月ごと、商品ごとの売上
    def montlyReport(self, calendar_data, product_name):
        product_sale = calendar_data[calendar_data["商品名"] == product_name]
        if (len(product_sale) == 0):
            return None
        product_sale["月"] = product_sale["日付"].apply(lambda x : int(x.split("-")[1]))
        fig, ax = plt.subplots(1,1, figsize=(5,5))
        # 箱ひげ図は「boxplot」を使う
        sns.boxplot(x="月", y="販売個数", data=product_sale)
        filePath = 'images/product_trend/product_%s_montlyplot.png' % product_name
        plt.savefig(filePath)


    #商品ごとの分布図の出力
    def scatterGraph(self, calendar_data, product_name):

        product_sale = calendar_data[calendar_data["商品名"] == product_name]
        if (len(product_sale) == 0):
            return None
        product_sale = self.dropOutlier(product_sale)

        fig = plt.figure()

        print("商品名:", product_name)

        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_title(product_name + " 平均気温")
        ax1.scatter(product_sale["平均気温(℃)"], product_sale["販売個数"])

        self.calcCorrelation(product_sale, "平均気温(℃)")

        ax2 = fig.add_subplot(2, 1, 2)
        ax2.set_title(product_name + " 平均風速")
        ax2.scatter(product_sale["平均風速(m/s)"], product_sale["販売個数"])

        self.calcCorrelation(product_sale, "平均風速(m/s)")

        filePath = 'images/product_trend/product_%s_liner.png' % product_name
        plt.savefig(filePath)

    #相関係数の出力
    def calcCorrelation(self, product_sale, keyword):
        s1=pd.Series(product_sale[keyword].values)
        s2=pd.Series(product_sale["販売個数"].values)
        res=s1.corr(s2)
        print(keyword , " 相関係数:", res)

    #箱ひげ図の出力
    def saveProductImage(self, calendar_data, product_name):
        product_sale = calendar_data[calendar_data["商品名"] == product_name]
        if (len(product_sale) == 0):
            return None

        product_sale = self.dropOutlier(product_sale)

        #ヒストグラム
        #trend_p1["販売個数"].hist(bins=20);
        #plt.savefig('images/product_1_histogram.png')
        #csvへのプロット
        #trend_p1.to_csv('trend_p1.csv', index=False)
        fig, ax = plt.subplots(1,5, figsize=(20,5))
        # 箱ひげ図は「boxplot」を使う
        keyWordArr = ["給料日", "休日", "六輝", "曜日","天気概況(夜：18時～翌日06時)"]
        index = 0
        for keyword in keyWordArr:
            sns.boxplot(x=keyword, y="販売個数", data=product_sale, ax=ax[index])
            index = index + 1

        filePath = 'images/product_trend/product_%s_boxplot.png' % product_name
        plt.savefig(filePath)


m = main()

#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#test_train_data = m.mergeData(m.sales_train_data)
#test_train_data = m.processMissingValue(test_train_data)
#m.plotting(test_train_data)

total_calendar_data = m.dataProcessing()
m.makeModel(total_calendar_data)