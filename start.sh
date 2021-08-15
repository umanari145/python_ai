pip install -r requirements.txt
cd /
curl -L  "https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00401.zip" > font.zip
unzip font.zip
cp IPAexfont00401/ipaexg.ttf /usr/local/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/ipaexg.ttf
echo "font.family : IPAexGothic" >>  /usr/local/lib/python3.9/site-packages/matplotlib/mpl-data/matplotlibrc
rm -rf /root/.cache