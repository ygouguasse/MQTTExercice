import RPi.GPIO as GPIO
import dht11
import time
import paho.mqtt.client as mqtt


# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 17)

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe("$sys/#")
#def on_message(client, userdata, msg):

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect

mqttc.connect("10.4.1.202",1883, 60)

while True:

    result = instance.read()

    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
        mqttc.loop()
        mqttc.publish("YounesCristelle/temperature", result.temperature, qos=1)
        mqttc.publish("YounesCristelle/Humidity", result.humidity, qos=1)
    else:
        print("Error: %d" % result.error_code)

    time.sleep(7)

