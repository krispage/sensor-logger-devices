import json
import requests

identifier = 'my-identifier'
secret_key = 'secret-key'
server_url = 'http://127.0.0.1:5000/data'

data = {"foo": "bar"}

request_data = {
    "identifier": identifier,
    "data": data
}

res = requests.post(server_url, headers={'Authorization': 'Bearer ' + secret_key,
    "Content-Type": "application/json", "Accept": "application/json"},
    data=json.dumps(request_data))
res.close()

