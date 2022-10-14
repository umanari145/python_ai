## 参考
【キカガク流】人工知能・機械学習 脱ブラックボックス講座 - 初級編 -


## 機械学習の分類
- 教師あり学習(入力xと出力y)　・・ここが一番わかりやすい
  - 回帰：数値の予測(ex 部屋の広さから家賃を分類)
  - 分類：カテゴリーの予測(ex 赤ワインor 白ワイン)
- 教師なし学習(入力x)
  - クラスタリング(グルーピング　マーケティングなど)
  - 次元削減(データ減らしたり)
- 強化学習(データがないorほとんどない)


## 単回帰分析

例：部屋の広さと家賃
y:出力変数
x:入力変数(広さ、距離)

### モデルの作成
- Step1 「モデル」を決める(広さと家賃)
  データに基づいて数式の定義を見つける直線?曲線?<br>
  点をplotして数式の定義を行う→ y^(ハット) = ax+bのような・・・<br>
  データの中心化を行うと計算が楽になる
- Step2 「」