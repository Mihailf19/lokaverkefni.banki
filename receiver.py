from mqtt_as import MQTTClient, config
import asyncio
from machine import Pin
from servo import Servo
from time import sleep

config["ssid"] = "TskoliVESM"
config["wifi_pw"] = "Fallegurhestur"
config["server"] = "test.mosquitto.org"
config["queue_len"] = 1

TOPIC = "Lock-Box"   

# Servo setup
servo_pin = Pin(15)
my_servo = Servo(servo_pin)
delay = 0.01
min_ang = 25
max_ang = 180
box_open = False

async def mottakari(client):
    global box_open
    async for topic, skilabod, _ in client.queue:
        msg = skilabod.decode()
        print("Received.")
        if msg == "TOGGLE":
            if not box_open:
                for i in range(min_ang, max_ang):
                    my_servo.write_angle(i)
                    sleep(delay)
                box_open = True
            else:
                for i in range(max_ang, min_ang, -1):
                    my_servo.write_angle(i)
                    sleep(delay)
                box_open = False

async def askrift(client):
    while True:
        await client.up.wait()
        client.up.clear()
        await client.subscribe(TOPIC, 1)

async def main(client):
    await client.connect()
    asyncio.create_task(askrift(client))
    asyncio.create_task(mottakari(client))
    while True:
        await asyncio.sleep_ms(0)

MQTTClient.DEBUG = True
client = MQTTClient(config)

try:
    asyncio.run(main(client))
finally:
    client.close()


