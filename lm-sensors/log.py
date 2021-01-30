import json
import requests
import datetime
import subprocess

identifier = 'my-identifier'
secret_key = 'secret-key'
server_url = 'http://my-server:5000/data'


def write_to_file():
    print("Couldn't connect. Writing to file for later")

    try:
        request_data['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('data/' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.json', 'a', encoding='utf-8') as f:
            json.dump(request_data, f, ensure_ascii=False, indent=2)
    except:
        print("error writing to file")



print("---------")
print(datetime.datetime.now())

sensors = subprocess.run(['sensors'], capture_output=True, text=True).stdout.replace(' ', '').split("\n")

def find_between(string, start, end):
    return string[string.index(start)+len(start):string.index(end)]

data = {
    "cpu_power":   find_between(sensor[sensor.index("fam15h_power-pci-00c4")+2], 'power1:', 'W(crit'),
    "fan_speed":   find_between(sensor[sensor.index("it8721-isa-0290")+11], 'fan1:',   'RPM'),
    "temp1":       find_between(sensor[sensor.index("it8721-isa-0290")+14], 'temp1:+', '°C'),
    "temp2":       find_between(sensor[sensor.index("it8721-isa-0290")+15], 'temp2:+', '°C'),
    "nic-temp1":   find_between(sensor[sensor.index("qlcnic-pci-0100")+2], 'temp1:+', '°C')
}

print('-------')

request_data = {
    "identifier": identifier,
    "data": data
}

success = True
try:
    res = requests.post(server_url, headers={'Authorization': 'Bearer ' + secret_key, 
        "Content-Type": "application/json", "Accept": "application/json"}, 
        data=json.dumps(request_data))
    res.close()
    if not res.status_code // 100 == 2:
        print("Error: Unexpected res {}".format(res)) 
        success = False
        write_to_file()
except requests.exceptions.RequestException:
        success = False 
        write_to_file()
finally:
    if success:
        print("success")
