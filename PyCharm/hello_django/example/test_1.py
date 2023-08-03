from urllib.parse import urlencode
from urllib.request import Request, urlopen

url = "http://localhost:8000"
data = {
    "name": "김석훈",
    "email": "shkim@naver.com",
    "url": "https://www.naver.com"
}

encData = urlencode(data)
postData = bytes(encData, encoding="utf-8")
req = Request(url, data=postData)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
f = urlopen(req)
print(f.headers)
print(f.read(500).decode("utf-8"))