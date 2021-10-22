#!venv/bin/python3 -u

import paho.mqtt.client
import serial as ser
import time
import paho

MQTT_TOPIC = 'home/nfc/0/serial'

mqtt = paho.mqtt.client.Client(client_id='nfc0')

def main():
    print('connecting to mqtt')
    mqtt.connect('home')
    print('connected to mqtt')
    mqtt.loop_start()

    port = ser.Serial()
    port.port = '/dev/ttyUSB0'
    port.baudrate = 115200
    port.open()

    buffer = []

    last_serial = ''
    next_scan = 0

    try:
        while True:
            char = port.read()
            if char == b'\r':
                serial = bytes(buffer).decode()
                buffer.clear()

                if serial == last_serial and time.time() < next_scan:
                    continue

                next_scan = time.time() + 5
                last_serial = serial
                handle_serial(serial)
            else:
                buffer.extend(char)
    except Exception as e:
        pass

    port.close()


def handle_serial(serial: str):
    print(f'serial: {serial}')
    mqtt.publish(MQTT_TOPIC, serial)


if __name__ == '__main__':
    main()
