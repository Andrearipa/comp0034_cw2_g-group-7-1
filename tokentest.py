'''from authlib.jose import JsonWebSignature as jws

protected = {'alg': 'HS256'}
payload = b'example'
secret = b'secret'
jws.serialize_compact(__self__, protected=protected, payload=payload, key=secret)


#s = JWS.serialize_json(header, payload, key)
'''

from jose import jws
from IPython.display import display
import json

signed = jws.sign({'a': 123456789}, 'secret', algorithm='HS256')
display(signed)
result = jws.verify(signed, 'secret', algorithms=['HS256']).decode('utf-8')

display(result)
# single_value = type(result)
single_value = json.loads(result)
display(type(single_value))
display(single_value['a'])


