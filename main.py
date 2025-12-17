from machine import Pin
import dht
import time
from machine import ADC   # LS, SMS
import os   # CSV
import utime

sensor = dht.DHT11(Pin(4))   # AM & T: air moisture en teperatur
ldr = ADC(26)   # LS: GP26 = lait sensor
SMS = ADC(25)   # SMS: soil moisture sensor
knop1 = Pin(14, Pin.IN, Pin.PULL_UP)
knop2 = Pin(32, Pin.IN, Pin.PULL_UP)

teller = 0
old_teller = 0

bestandsnaam = "metingen.csv"


def print_csv():

    try:
        with open(bestandsnaam, "r") as f:
            print("=== START_CSV ===")

            for regel in f:
                print(regel.strip())

            print("=== END_CSV ===")

    except OSError:
        print("CSV-bestand niet gevonden!")


while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        waarde_LS = ldr.read_u16()   # LS: 0–65535
        waarde_SMS = SMS.read_u16()   # SMS: 0–65535

        #print("Temperatuur:", temp, "°C")
        #print("Luchtvochtigheid:", hum, "%")
        #print(waarde_LS)   # LS
        #print(waarde_SMS)   # SMS
        #print(f"{temp:.2f},{hum:.2f}")
        #print("")

        # Check of CSV bestand al bestaat
        if bestandsnaam not in os.listdir():
            with open(bestandsnaam, "w") as f:
                f.write("tijd,waarde\n")

        # Data toevoegen aan CSV
        if (teller == old_teller + 10):
            with open(bestandsnaam, "a") as f:
                f.write(f"{utime.time()},{temp},{hum},{waarde_LS},{waarde_SMS}\n")

            old_teller = teller

        if knop1.value() == 0:
            print_csv()

            time.sleep(0.5)

            while knop1.value() == 0:
               time.sleep(0.5)


        if knop2.value() == 0:
            with open(bestandsnaam, "w") as f:
                pass

        teller = teller + 1

        #print(teller, old_teller)

    except OSError as e:

        print("Fout bij lezen van sensor:", e)

    time.sleep(1)
