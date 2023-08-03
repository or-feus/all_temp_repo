from urllib.request import HTTPBasicAuthHandler, build_opener

auth_handler = HTTPBasicAuthHandler()
auth_handler.add_password(realm="ksh", user="shkim", passwd="shkimadmin", uri="http://localhost:8000/auth")
opener = build_opener(auth_handler)
resp = opener.open("http://localhost:8000/auth/")
print(resp.read().decode("utf-8"))