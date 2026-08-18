from machine import Pin
import sys
import uselect
import time

# LEDS

rojo = Pin(26, Pin.OUT)
verde = Pin(27, Pin.OUT)

# PULSADORES

pulsador_verde = Pin(12, Pin.IN, Pin.PULL_UP)
pulsador_rojo = Pin(14, Pin.IN, Pin.PULL_UP)

# ESTADO YOLO

deteccion_yolo = ""

# SERIAL

poll = uselect.poll()
poll.register(sys.stdin, uselect.POLLIN)

print("================================")
print("ESP32 LISTO")
print("GPIO 12 -> Pulsador VERDE")
print("GPIO 14 -> Pulsador ROJO")
print("GPIO 27 -> LED VERDE")
print("GPIO 26 -> LED ROJO")
print("Esperando YOLO...")
print("================================")

# BUCLE PRINCIPAL

while True:

    # RECIBIR YOLO

    eventos = poll.poll(10)

    if eventos:

        dato = sys.stdin.readline().strip()

        print("Recibido:", dato)

        if dato == "CARRO":

            deteccion_yolo = "CARRO"

        elif dato == "MOTO":

            deteccion_yolo = "MOTO"

        elif dato == "NINGUNO":

            deteccion_yolo = ""

    # LEER PULSADORES

    boton_verde = pulsador_verde.value() == 0
    boton_rojo = pulsador_rojo.value() == 0

    # PRIORIDAD PULSADORES

    if boton_rojo:

        rojo.value(1)
        verde.value(0)

    elif boton_verde:

        rojo.value(0)
        verde.value(1)

    # YOLO

    elif deteccion_yolo == "CARRO":

        rojo.value(1)
        verde.value(0)

    elif deteccion_yolo == "MOTO":

        rojo.value(0)
        verde.value(1)

    else:

        rojo.value(0)
        verde.value(0)

    time.sleep_ms(10)
