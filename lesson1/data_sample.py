import pandas as pd 

df = pd.read_csv('students.csv', index_col='生徒番号')
#一般的な表示
print("--全体的な表示--")
print(df)
print("--特定のカラムのみ表示--")
print(df['握力'])


