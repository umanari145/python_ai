import os
from dotenv import load_dotenv
import pandas as pd
import database
import analysis
import analysisDate

# .envファイルの内容を読み込みます
load_dotenv()

# os.environを用いて環境変数を表示させます
db = database.database({
    'DB_HOST' : os.environ['DB_HOST'],
    'DB_NAME' : os.environ['DB_NAME'],
    'DB_USER' : os.environ['DB_USER'],
    'DB_PASS' : os.environ['DB_PASS']
})

anaDate = analysisDate.analysisDate(db)
anaDate.rewardsCheck()
#anaDate.sample()
#ana = analysis.analysis(db)
#ana.rewardsCheck()
#ana.memberCheck()
#ana.oligopoly()