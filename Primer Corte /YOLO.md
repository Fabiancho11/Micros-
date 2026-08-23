
<h2 align="left"><b>Desarrollo del esquema en Wokwi</b></h2>

<p>
Primero se desarrolló el siguiente esquema en Wokwi, utilizando una ESP32, dos LEDs y dos pulsadores. Cada pulsador está asociado a un LED, permitiendo controlar su encendido y apagado.
</p>

<p align="center">
  <img src="../Imagenes/Wokwi.png" alt="Esquema desarrollado en Wokwi" width="600">
</p>

<p align="center">
  <a href="https://wokwi.com/projects/473182162418344961" target="_blank">
    <b>Ver proyecto en Wokwi</b>
  </a>
</p>

<h2 align="center"><b>Desarrollo del código en MicroPython</b></h2>

<p>
Posteriormente, se desarrolló el código en <b>MicroPython</b> para programar el funcionamiento de la ESP32. El código permite encender y apagar cada LED mediante su respectivo pulsador.
</p>

<h3 align="center"><b>Código MicroPython</b></h3>

<pre>
<code>
from machine import Pin
import time

# ==========================================
# LEDS
# ==========================================
rojo = Pin(26, Pin.OUT)
verde = Pin(25, Pin.OUT)

# ==========================================
# PULSADORES
# ==========================================
pulsador_rojo = Pin(13, Pin.IN, Pin.PULL_UP)
pulsador_verde = Pin(14, Pin.IN, Pin.PULL_UP)

# ==========================================
# BUCLE PRINCIPAL
# ==========================================
while True:

    # CONTROL POR PULSADORES
    if pulsador_rojo.value() == 0:
        rojo.value(1)
        verde.value(0)

    elif pulsador_verde.value() == 0:
        rojo.value(0)
        verde.value(1)

    else:
        rojo.value(0)
        verde.value(0)

    time.sleep_ms(10)

</code>
</pre>
