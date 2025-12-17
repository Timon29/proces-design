import serial
import matplotlib.pyplot as plt

ser = serial.Serial("COM10", 115200, timeout=1)

temps = []
hums = []
waardes_LS = []
waardes_SMS = []

plt.ion()
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10,12))


while True:
    lijn = ser.readline().decode().strip()

    if not lijn:
        continue

    #print("Ontvangen:", lijn)

    try:
        tijd, temp, hum, waarde_LS, waarde_SMS = map(float, lijn.split(","))

    except ValueError:
        continue

    temps.append(temp)
    hums.append(hum)
    waardes_LS.append(waarde_LS)
    waardes_SMS.append(waarde_SMS)

    ax1.clear()
    ax1.plot(temps, color="blue")
    ax1.set_ylabel("Temperatuur (°C)")
    ax1.set_xlabel("Meetpunten")
    ax1.set_title("Temperatuur")

    # Humidity grafiek
    ax2.clear()
    ax2.plot(hums, color='blue')
    ax2.set_ylabel("Humidity (%)")
    ax2.set_title("Humidity")
    ax2.set_xlabel("Meetpunten")

    ax3.clear()
    ax3.plot(waardes_LS, color='blue')
    ax3.set_ylabel("Lichtinval")
    ax3.set_title("Lichtinval")
    ax3.set_xlabel("Meetpunten")

    # vochtigheid aarde
    ax4.clear()
    ax4.plot(waardes_SMS, color='blue')
    ax4.set_ylabel("Vochtigheid aarde")
    ax4.set_title("Vochtigheid aarde")
    ax4.set_xlabel("Meetpunten")
    plt.pause(0.1)
