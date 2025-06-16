import os
import adafruit_requests
import wifi
import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time

wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
mqtt_topic = "zigbee2mqtt/Cube1"
radio = wifi.radio

while not radio.connected:
    radio.connect(wifi_ssid, wifi_password)
print("Connected to WiFi!")

# get the pool and ssl_context from the helpers:
pool = adafruit_connection_manager.get_radio_socketpool(radio)


def connected(client: MQTT.MQTT, userdata, flags, rc):
    print(f"Subscribing to {mqtt_topic}")
    client.subscribe(mqtt_topic)


def disconnected(client, userdata, rc):
    print("Disconnected from MQTT Broker!")


def message(client, topic, message):
    print(f"New message on topic {topic}: {message}")


mqtt_client = MQTT.MQTT(
    broker=os.getenv("MQTT_BROKER"),
    username=os.getenv("MQTT_USERNAME"),
    password=os.getenv("MQTT_PASSWORD"),
    is_ssl=False,
    socket_pool=pool
)


mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
mqtt_client.connect()

while True:
    # Poll the message queue
    mqtt_client.loop()

    time.sleep(1)
