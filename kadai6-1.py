import requests
import pandas as pd

APP_ID = "6c2c0b92e79b177a5dac164d5e6d7da4c9cb46dc"#自分のAPI
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"#エンドポイント
params = {
    "appId": APP_ID,
    "statsDataId": "0004009600",
    "cdArea": "12101,12102,12103,12104,12105,12106",
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
    "lang": "J"
}

res = requests.get(API_URL, params=params)
data = res.json()["GET_STATS_DATA"]["STATISTICAL_DATA"]

meta = data["CLASS_INF"]["CLASS_OBJ"]
if isinstance(meta, dict):
    meta = [meta]
    
#データの取得
values = data["DATA_INF"]["VALUE"]
df = pd.DataFrame(values)

#列のコードを名称に変換
for c in meta:
    col_key = "@" + c["@id"]
    mapping = {}
    cls = c["CLASS"]
    cls_list = cls if isinstance(cls, list) else [cls]
    for ent in cls_list:
        mapping[ent["@code"]] = ent["@name"]
    if col_key in df.columns:
        df[col_key] = df[col_key].replace(mapping)
        
#列名を日本語にする        
col_map = {"@unit": "単位", "$": "値"}
for c in meta:
    col_map["@"+c["@id"]] = c["@name"]
df.rename(columns=col_map, inplace=True)

print(df)
