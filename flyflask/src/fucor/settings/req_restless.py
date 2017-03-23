import requests
import json

url = 'http://127.0.0.1:5000/api/CM_TABLE'
headers = {'Content-Type': 'application/json'}

filters = [dict(name='name', op='like', val='%TM_CODEXH%')]
params = dict(q=json.dumps(dict(filters=filters)))

response = requests.get(url, params=params, headers=headers)
assert response.status_code == 200
print(response.json())
# http://localhost:5000/api/CM_TABLE?q={%22filters%22:[{%22name%22:%22name%22,%22op%22:%22like%22,%22val%22:%22TM_CODEXH%22}]}