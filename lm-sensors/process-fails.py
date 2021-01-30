import json
import requests
import os

identifier = 'my-identifier'
secret_key = 'secret-key'
server_url = 'http://my-server:5000/data'
directory  = 'data'

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            request_data = json_file.read()
            success = True
            try:
                res = requests.post(server_url, headers={'Authorization': 'Bearer ' + secret_key,
                    "Content-Type": "application/json", "Accept": "application/json"},
                    data=request_data)
                res.close()
            except requests.exceptions.RequestException:
                success = False
                print(file_path + " failed")
            finally:
                if success:
                    os.remove(file_path)
                    print(file_path + " success")
    else:
        continue

