from urllib.request import HTTPCookieProcessor, build_opener, Request

url = "http://localhost:8000/cookie/"
cookie_handler = HTTPCookieProcessor()
opener = build_opener(cookie_handler)

req = Request(url)
resp = opener.open(req)

print("< first Response after GET Request > \n")
print(resp.headers)
print(resp.read().decode("utf-8"))

print("--------------------------------------------")
data = "language=python&framework=django"
encData = bytes(data, encoding="utf-8")

req = Request(url, encData)
resp = opener.open(req)

print("< second Response after POST Request > \n")
print(resp.headers)
print(resp.read().decode("utf-8"))
