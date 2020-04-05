# covid19_shizuoka-opendata_csv2json

「静岡県ふじのくにオープンデータカタログ」で公開されているCSVデータを  
「新型コロナウイルス感染症対策サイト」で利用しているdata.jsonへ変換するプロジェクトです。

Pythonバージョン : 3.6

## サポートデータ

### 検査実施人数
key : inspection_persons
|  都市  |  オープンデータ API URL  |
| ---- | ---- |
| 浜松 | https://opendata.pref.shizuoka.jp/api/package_show?id=d4827176-d887-412a-9344-f84f161786a2 |

### 新型コロナコールセンター相談件数
key : contacts
|  都市  |  オープンデータ API URL  |
| ---- | ---- |
| 浜松 | https://opendata.pref.shizuoka.jp/api/package_show?id=1b57f2c0-081e-4664-ba28-9cce56d0b314 |


### Ready comming soon

#### 検査陽性者の状況
key : main_summary
オープンデータ準備中

#### 陽性患者の属性
key : patients
|  都市  |  オープンデータ API URL  |
| ---- | ---- |
| 浜松 | https://opendata.pref.shizuoka.jp/api/package_show?id=5ab47071-3651-457c-ae2b-bfb8fdbe1af1 |


#### 陽性患者数
key : patients_summary
オープンデータ準備中

## 引数について

GraphType-key:API-IDの配列  
というような形式で引数指定できます。  
例 : inspection_persons:d4827176-d887-412a-9344-f84f161786a2,contacts:1b57f2c0-081e-4664-ba28-9cce56d0b314  

Pythonを直接実行する場合  
lambda_function.py.lambda_handlerのeventに以下のようなJSONを渡します。  
```
{
    "queryStringParameters": {
        "type": "inspection_persons:d4827176-d887-412a-9344-f84f161786a2,contacts:1b57f2c0-081e-4664-ba28-9cce56d0b314"
    }
}
```

コマンドライン実行例  
```
python -c "import os; os.chdir('source'); import lambda_function; x = lambda_function.lambda_handler({'queryStringParameters':None}, None); print(x['body'])" > data.json
python -c "import os; os.chdir('source'); import lambda_function; x = lambda_function.lambda_handler({'queryStringParameters':{'type':'contacts:1b57f2c0-081e-4664-ba28-9cce56d0b314'}}, None); print(x['body'])" > data.json
```

API Gateway経由でLambdaを実行する場合  
API GatewayのGETでクエリパラメータに以下のように指定します。  
```
?type=inspection_persons:d4827176-d887-412a-9344-f84f161786a2,contacts:1b57f2c0-081e-4664-ba28-9cce56d0b314  
```
