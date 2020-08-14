# covid19_shizuoka-opendata_csv2json

「静岡県ふじのくにオープンデータカタログ」で公開されているCSVデータを  
「新型コロナウイルス感染症対策サイト」で利用しているdata.jsonへ変換するプロジェクトです。

Pythonバージョン : 3.6

## サポートデータ

| 名称 | COVID-19サイトのデータタイプKEY | オープンデータカタログID(浜松市用) | オープンデータカタログID(静岡市用) |
| --- | --- | --- | --- |
| 検査陽性者の状況 | main_summary | 5ab47071-3651-457c-ae2b-bfb8fdbe1af1 | c04e2d2f-2ce4-4e32-856a-b7e760ba982d |
| 陽性患者の属性 | patients | 5ab47071-3651-457c-ae2b-bfb8fdbe1af1 | c04e2d2f-2ce4-4e32-856a-b7e760ba982d |
| 陽性患者数 | patients_summary | 5ab47071-3651-457c-ae2b-bfb8fdbe1af1 | c04e2d2f-2ce4-4e32-856a-b7e760ba982d |
| 検査実施人数 | inspection_persons| d4827176-d887-412a-9344-f84f161786a2 | 6b102a25-9746-4dac-b6a9-8370afe6af75 |
| 新型コロナウイルス感染症に関する相談件数| contacts | 1b57f2c0-081e-4664-ba28-9cce56d0b314 | 4e25348c-b24d-4bc5-b85b-dac9e2fd2439 |


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

## その他
「検査陽性者の状況」と「陽性患者数」は、「陽性患者の属性」のデータから生成します。


## ライブラリのインストール
$ pip install -r requirements.txt -t source

## パッケージング&デプロイ コマンド
$ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
$ cd source
$ zip -r ../lambda-package.zip *
$ aws lambda update-function-code --function-name {{your function name}} --zip-file fileb://../lambda-package.zip
