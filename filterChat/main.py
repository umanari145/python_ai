import os
from dotenv import load_dotenv
import pandas as pd
import database
import analysis

# .envファイルの内容を読み込みます
load_dotenv()

# os.environを用いて環境変数を表示させます
db = database.database({
    'DB_HOST' : os.environ['DB_HOST'],
    'DB_NAME' : os.environ['DB_NAME'],
    'DB_USER' : os.environ['DB_USER'],
    'DB_PASS' : os.environ['DB_PASS']
})
#db.select("select * from month")
rewards = db.select("select target_month, SUM(dmm_point + no_dmm_point + other_point) as total_point from rewards where is_delete = 0 group by target_month" )
for reward in rewards:
    reward['target_month'] = str(reward['target_month'])[2:4] + "/" + str(reward["target_month"])[4:7]
db.close()

ana = analysis.analysis()
ana.rewards(rewards)


