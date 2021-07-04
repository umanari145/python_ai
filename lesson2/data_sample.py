import pandas as pd 
import numpy as np
df = pd.read_csv('students2.csv', index_col='生徒番号')
print("英語の点数順番に表示")
df2 = df.sort_values('英語', ascending=False)
print(df2)
print("トップ10表示")
top_score = np.array(df2['英語'])[:10]
print(top_score)
print("全平均")
top_score = np.array(df2['英語'])
#print(sum(top_score))
#平均=合計/配列数
print(sum(top_score) / len(top_score))
#一発で平均がでる
print(np.mean(df['英語']))
print("中央値")
print(np.median(df['英語']))

print("最頻値")
print("1と2がもっともよく出てくる値")
#最頻値
print(pd.Series([1,1,1,2,2,2,3,3]).mode())

print("偏差")
simple_score=np.array(df2['英語'])
deviation=simple_score-np.mean(simple_score)
print(deviation)
print(np.mean(deviation))

df2['偏差']=deviation
#df2['偏差二乗']=deviation ** 2
df2['偏差二乗']=np.square(deviation)
print(df2)