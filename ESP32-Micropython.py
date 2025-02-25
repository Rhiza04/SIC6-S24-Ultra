from machine import Pin, ADC
import ujson
import network
import utime as time
import dht
import urequests as requests
import sys

ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)
dht_sensor = dht.DHT22(Pin(15))
pir_sensor = Pin(35, Pin.IN) 

DEVICE_ID = "esp32-sic6"
WIFI_SSID = "3R"
WIFI_PASSWORD = "kc27baruga"
TOKEN = "BBUS-eAU1dmQcS5okWqGT6RMayC0eBj3mzM"

UBIDOTS_URL = "https://stem.ubidots.com/api/v1.6/devices/" + DEVICE_ID
HEADERS = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}

wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Connecting to WiFi...")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

timeout = 30 
while not wifi_client.isconnected() and timeout > 0:
    print("Connecting...")
    time.sleep(1)
    timeout -= 1

if wifi_client.isconnected():
    print("WiFi Connected!", wifi_client.ifconfig())
else:
    print("❌ Failed to connect to WiFi. Check credentials.")
    sys.exit()

def send_data(temperature, humidity, light, motion):
    data = {
        "temperature": {"value": temperature},
        "humidity": {"value": humidity},
        "light": {"value": ldr_value},
        "motion": {"value": motion}
    }
    try:
        response = requests.post(UBIDOTS_URL, json=data, headers=HEADERS)
        print("✅ Data ke Ubidots terkirim!")
        print("Response:", response.text)
    except Exception as e:
        print("❌ Gagal mengirim data ke Ubidots:", e)
        
    try:
        response_flask = requests.post(FLASK_ENDPOINT, json=data)
        print("✅ Data ke Flask terkirim!")
        print("Response Flask:", response_flask.text)
    except Exception as e:
        print("❌ Gagal mengirim data ke Flask:", e)
        
FLASK_ENDPOINT = f"http://192.168.1.19:5000"
while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        ldr_value = ldr.read()
        motion = pir_sensor.value() 

        print(f"Temp: {temperature}, Humidity: {humidity}, Light: {ldr_value}, Motion: {motion}")
        send_data(temperature, humidity, ldr_value, motion)

    except Exception as e:
        print("❌ Sensor reading error:", e)

    time.sleep(1) 
