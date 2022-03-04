'''from authlib.jose import JsonWebSignature as jws

protected = {'alg': 'HS256'}
payload = b'example'
secret = b'secret'
jws.serialize_compact(__self__, protected=protected, payload=payload, key=secret)


#s = JWS.serialize_json(header, payload, key)
'''

from jose import jws
from IPython.display import display

signed = jws.sign({'a': 'b'}, 'secret', algorithm='HS256')
display(signed)
result = jws.verify(signed, 'secret', algorithms=['HS256'])
display(result)


