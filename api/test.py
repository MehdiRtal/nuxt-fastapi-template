from jose import jwt 

secret = "secret"

token = jwt.encode({"sub": "123"}, secret, algorithm="HS256")

print(token)


payload = jwt.get_unverified_header(token)
print(payload)
payload = jwt.decode(token, secret, algorithms=["HS256"])
print(payload)