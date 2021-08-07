import os
from dotenv import load_dotenv
import database

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

db.select("select * from rewards where user_id = %s", [102])
db.close()
