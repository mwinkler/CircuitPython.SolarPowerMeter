import wifi
import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time

class MqttConnector:
    def __init__(self, host: str, username: str=None, password: str=None):
        self._connected = False
        self._subscribed_topics = {}

        self._mqtt_client = MQTT.MQTT(
            broker=host,
            username=username,
            password=password,
            is_ssl=False,
            socket_pool=adafruit_connection_manager.get_radio_socketpool(wifi.radio)
        )

        def on_connect(client, userdata, flags, rc):
            print("Connected to MQTT Broker!")
            self._connected = True
        
        def on_disconnect(client, userdata, rc):
            print("Disconnected from MQTT Broker!")
            self._connected = False
        
        def on_message(client, topic, message):
            print(f"New message on topic {topic}: {message}")
            if topic in self._subscribed_topics:
                self._subscribed_topics[topic](message)

        self._mqtt_client.on_connect = on_connect
        self._mqtt_client.on_disconnect = on_disconnect
        self._mqtt_client.on_message = on_message

    def _check_connection(self):
        if self._connected:
            return
        
        print("Connecting to MQTT Broker...")
        self._mqtt_client.connect()
        
        # Wait for connection to be established
        retries = 0
        while not self._connected and retries < 5:
            print("Waiting for MQTT connection...")
            time.sleep(1)
            retries += 1
        if not self._connected:
            raise RuntimeError("Failed to connect to MQTT Broker after 5 retries.")

    def subscribe(self, mqtt_topic: str, callback):
        print(f"Subscribing to {mqtt_topic}")
        self._check_connection()
        self._mqtt_client.subscribe(mqtt_topic)
        self._subscribed_topics[mqtt_topic] = callback

    # Poll the MQTT client to handle network traffic and dispatch callbacks.
    def poll(self):
        self._check_connection()
        self._mqtt_client.loop()
