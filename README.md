# python_ai

参考リンク<br>

https://github.com/ghmagazine/python_stat_sample

## ライブラリインストール
```
pip install -r requirements.txt
```

lesson1 イントロ
lesson2 一次元データの整理

select 
	target_month, 
	u.id as userId,
	u.`japanese_name`, 
	(r.dmm_point + r.no_dmm_point + r.other_point) as total_point,
	(r.dmm_point + r.no_dmm_point + r.other_point) / (select sum(dmm_point + no_dmm_point + other_point) from rewards r2 where r2.target_month = r.target_month) * 100 as percent
from rewards r 
	left join users u on r.user_id = u.id 
	where r.is_delete = 0 
	order by target_month, total_point desc;