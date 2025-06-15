import requests
#オープンデータは"openBD"
isbn = "978-4-7741-9690-9"
url = f"https://api.openbd.jp/v1/get?isbn={isbn}"#エンドポイント

# APIへリクエストを送信
response = requests.get(url)
data = response.json()

# 結果を表示
if data[0] is not None:
    summary = data[0]["summary"]
    print(f"著者名: {summary.get('author', 'N/A')}")
    print(f"書名: {summary.get('title', 'N/A')}")
    print(f"出版社名: {summary.get('publisher', 'N/A')}")
    print(f"出版年月: {summary.get('pubdate', 'N/A')}")
    print(f"書影URL: {summary.get('cover', 'N/A')}")
else:
    print("指定したISBNの書籍データは見つかりませんでした。")
