# SENDER

from machine import Pin, SoftI2C, SPI          
from neopixel import NeoPixel                  
from I2C_LCD import I2cLcd                     
from mfrc522 import MFRC522                    
import uasyncio as asyncio                     
from mqtt_as import MQTTClient, config         

# WiFi og MQTT stillingar
config["ssid"] = "TskoliVESM"
config["wifi_pw"] = "Fallegurhestur"
config["server"] = "test.mosquitto.org"

TOPIC = "Lock-Box"                            

# NeoPixel stillingar
neo_pin = Pin(4, Pin.OUT)
neo = NeoPixel(neo_pin, 2)
neo.fill([0, 0, 0]); neo.write()               # Slökkva á öllum ljósum

# Litir
blue  = [0, 255, 0]
red   = [0, 0, 255]
off   = [0, 0, 0]

# LCD skjár stilltur yfir I2C
i2c = SoftI2C(scl=Pin(3), sda=Pin(8), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)
lcd.clear(); lcd.putstr("Scan your card.")     # Byrjunartexti

# RFID lesari stilltur yfir SPI
spi = SPI(2, baudrate=2500000, polarity=0, phase=0,
          sck=Pin(12), mosi=Pin(11), miso=Pin(13))
rfid = MFRC522(spi, 10, 9)

# Rétt RFID kort (leyfilegt kort)
f0 = [195, 184, 214, 29, 176]

# Sérsniðin tákn (læst og ólæst) fyrir LCD
locked = [
    0b00000,
    0b01110,
    0b10001,
    0b10001,
    0b11111,
    0b11011,
    0b11011,
    0b11111
]
lcd.custom_char(0, locked)

unlocked = [
    0b00000,
    0b01110,
    0b10001,
    0b10000,
    0b11111,
    0b11011,
    0b11011,
    0b11111
]
lcd.custom_char(1, unlocked)

# Fall sem bíður eftir RFID korti
async def scan_card():
    while True:
        (stat, _) = rfid.request(rfid.REQIDL)  
        if stat == rfid.OK:
            (stat, uid) = rfid.anticoll()      # Les UID af korti
            if stat == rfid.OK:
                return uid                     # Skilar kortanúmeri
        await asyncio.sleep(0.05)              # Lítill biðtími

# Aðalforrit sem keyrir MQTT og korthandling
async def main(client):
    await client.connect()                     # Tengist MQTT
    while True:
        uid = await scan_card()                # Biður um kort
        lcd.clear()
        if uid == f0:                          # Rétt kort fundið
            lcd.putstr("Access Granted  ")
            lcd.putchar(chr(1))                # Sýna ólæst tákn
            neo[0] = red; neo[1] = blue; neo.write()
            print("Access Granted")
            await client.publish(TOPIC, b"TOGGLE")  # Sendir skilaboð
        else:
            lcd.putstr("Unknown card ")
            lcd.putchar(chr(0))                # Sýna læst tákn
            neo[0] = blue; neo[1] = red; neo.write()
            print("Unknown card.")

        await asyncio.sleep(1.5)               # Bið áður en verkið endurræsist
        lcd.clear(); lcd.putstr("Scan your card.")
        neo.fill(off); neo.write()             # Slökkva ljós

# Setur upp MQTT viðskiptavin
MQTTClient.DEBUG = True
client = MQTTClient(config)

# Keyrir og lokar ef villa kemur upp
try:
    asyncio.run(main(client))
finally:
    client.close()

