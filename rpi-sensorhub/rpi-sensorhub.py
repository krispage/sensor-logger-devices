import smbus
import json
import requests

identifier = 'my-rpi-sensorhub'
secret_key = 'secret-key'
server_url = 'http://127.0.0.1:5000/data'

# From https://wiki.52pi.com/index.php/DockerPi_Sensor_Hub_Development_Board_SKU:_EP-0106

DEVICE_BUS = 1
DEVICE_ADDR = 0x17

TEMP_REG = 0x01
LIGHT_REG_L = 0x02
LIGHT_REG_H = 0x03
STATUS_REG = 0x04
ON_BOARD_TEMP_REG = 0x05
ON_BOARD_HUMIDITY_REG = 0x06
ON_BOARD_SENSOR_ERROR = 0x07
BMP280_TEMP_REG = 0x08
BMP280_PRESSURE_REG_L = 0x09
BMP280_PRESSURE_REG_M = 0x0A
BMP280_PRESSURE_REG_H = 0x0B
BMP280_STATUS = 0x0C
HUMAN_DETECT = 0x0D

bus = smbus.SMBus(DEVICE_BUS)

aReceiveBuf = []

aReceiveBuf.append(0x00)

data = {}

for i in range(TEMP_REG,HUMAN_DETECT + 1):
    aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

if aReceiveBuf[STATUS_REG] & 0x01 :
    data['offchip_temperature'] = -100
elif aReceiveBuf[STATUS_REG] & 0x02 :
    data['offchip_temperature'] = -100
else :
    data['offchip_temperature'] = aReceiveBuf[TEMP_REG]


if aReceiveBuf[STATUS_REG] & 0x04 :
    data['light'] = -100
elif aReceiveBuf[STATUS_REG] & 0x08 :
    data['light'] = -100
else :
    data['light'] = (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L])

data['onboard_temperature'] = aReceiveBuf[ON_BOARD_TEMP_REG]
data['onboard_humidity'] = aReceiveBuf[ON_BOARD_HUMIDITY_REG]

if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
    data['onboard_temperature'] = aReceiveBuf[ON_BOARD_TEMP_REG]
    data['onboard_humidity'] = aReceiveBuf[ON_BOARD_HUMIDITY_REG]


if aReceiveBuf[BMP280_STATUS] == 0 :
    data['barometer_temperature'] = aReceiveBuf[BMP280_TEMP_REG]
    data['barometer_pressure'] = (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16)
else :
    data['barometer_temperature'] = -100
    data['barometer_pressure'] = -100


data['movement_sensor'] = aReceiveBuf[HUMAN_DETECT]


request_data = {
    "identifier": identifier,
    "data": data
}

res = requests.post(server_url, headers={'Authorization': 'Bearer ' + secret_key,
    "Content-Type": "application/json", "Accept": "application/json"},
    data=json.dumps(request_data))
res.close()

