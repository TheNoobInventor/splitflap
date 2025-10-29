import time

from umqtt.simple import MQTTClient

from typing import Union, Tuple, Dict
from Message import Message
from Source import Source
from provider.Provider import Provider

from primary.Display import Display
from primary.ISSLocation import iss_location

# MQTT connection setup
MQTT_ClientID = 'Splitflap'
BROKER = '192.168.change.me' # Input your MQTT broker IP address
USER = 'mqtt_broker'         # Input username if required by broker
PASSWORD = 'change-me'       # Input password if required by broker
TOPIC = 'splitflap/commands'


class SourceMQTT(Source):
    def __init__(self, display: Display, providers: Dict[str, Provider]):
        self.display = display
        self.providers = providers
        self.default_provider = Provider()

        # MQTT callback function
        def load_mqtt_message(topic, msg):

            # Decode message received via the broker
            decoded_mqtt_message = msg.decode()

            if decoded_mqtt_message and decoded_mqtt_message != self.previous_mqtt_message:
                # Run the ISS script which either returns the country the ISS is over
                # or ERROR signifying that it's over an ocean, these will be displayed
                # by the split flap
                if decoded_mqtt_message == "whereami":
                    self.current_mqtt['text'] = iss_location()

                # Reset the split flap display by showing the empty character
                elif decoded_mqtt_message == "reset":
                    self.current_mqtt_message['text'] = "        "

                # Otherwise display whatever was sent via the broker
                else:
                    self.current_mqtt_message['text'] = decoded_mqtt_message

                self.scheduled_time = time.ticks_ms()
                self.previous_mqtt_message = decoded_mqtt_message

        # Connect to MQTT broker
        self.client = MQTTClient(MQTT_ClientID, BROKER, user=USER, password=PASSWORD)
        print(f"Connected to MQTT broker: {BROKER}") # delete later
        self.client.connect()
        self.client.set_callback(load_mqtt_message)
        self.client.subscribe(TOPIC)
        self.current_mqtt_message = {}
        self.previous_mqtt_message = {}

    #
    def display_data_to_message(self, display_data: Dict[str, str], physical_motor_position: [int]) -> Tuple[Message, int]:
        motor_pos = self.display.physical_to_virtual(physical_motor_position)
        text = display_data['text'].upper()
        provider = self.providers.get(text, self.default_provider)
        message, interval_ms = provider.get_message(text, display_data, self.display, motor_pos)
        return self.display.virtual_to_physical(message), interval_ms

    #
    def load_message(self, is_stopped: bool, physical_motor_position: [int]) -> Union[Message, None]:

        if not is_stopped:
            return None

        # Check for messages from the MQTT broker
        self.client.check_msg()

        # Check if there's new data on the topic and if the current mqtt message does not have the value of None
        if self.current_mqtt_message and self.current_mqtt_message != self.previous_mqtt_message:    

            message, interval = self.display_data_to_message(self.current_mqtt_message, physical_motor_position)

            # Set the current MQTT message as the previous one
            self.previous_mqtt_message = self.current_mqtt_message

            return message

        return None
 
    # TODO: 
    # Sort out function comments
    # Move calibration_test.py into Calibrate.py
