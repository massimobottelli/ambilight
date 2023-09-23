import paho.mqtt.client as mqtt
import config
import pigpio
import threading
import signal

# Set GPIO pins
PIN_R = 17
PIN_G = 22
PIN_B = 24

# Access the constants from the config module
broker_ip = config.broker_ip
topic = config.topic
username = config.username
password = config.password

# Initialize pigpio once
pi = pigpio.pi()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        print("Listening...")
        client.subscribe(topic)
    else:
        print("Connection failed. RC:", rc)

def on_message(client, userdata, msg):
    color_R, color_G, color_B = map(int, msg.payload.decode().split(","))

    print(color_R, color_G, color_B)

    pi.set_PWM_dutycycle(PIN_R, color_R)
    pi.set_PWM_dutycycle(PIN_G, color_G)
    pi.set_PWM_dutycycle(PIN_B, color_B)

# Create a threading event to gracefully exit the script
exit_event = threading.Event()

def exit_handler(signal, frame):
    print("Exiting the script...")
    pi.stop()
    exit_event.set()

# Set up a signal handler for Ctrl+C
signal.signal(signal.SIGINT, exit_handler)

# Main
if __name__ == '__main__':
    # Receive the angles via MQTT listener
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_ip)
    client.loop_start()

    try:
        while not exit_event.is_set():
            pass
    except KeyboardInterrupt:
        pass

    # Ensure a clean exit
    client.loop_stop()
