from jose import jws
signed = jws.sign({'a': 'b'}, 'secret', algorithm='HS256')

print(signed)

print(jws.verify(signed, 'secret', algorithms=['HS256']))

