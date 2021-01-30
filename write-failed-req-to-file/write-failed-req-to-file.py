import json
import requests
import datetime

identifier = 'my-identifier'
secret_key = 'secret-key'
server_url = 'http://127.0.0.1:5000/data'

data = {"foo": "bar"}

request_data = {
    "identifier": identifier,
    "data": data
}


try:
    res = requests.post(server_url, headers={'Authorization': 'Bearer ' + secret_key, 
        "Content-Type": "application/json", "Accept": "application/json"}, 
        data=json.dumps(request_data))
    res.close()
except requests.exceptions.RequestException:
    print("Couldn't connect. Writing to file for later")

    try:
        request_data['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('data/' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.json', 'a', encoding='utf-8') as f:
            json.dump(request_data, f, ensure_ascii=False, indent=2)
    except:
        print("boo :(")


