
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

<h1><b>Implementación de YOLO para la detección de motos y carros</b></h1>

<h2><b>¿Qué es YOLO?</b></h2>

<p>
<b>YOLO (You Only Look Once)</b> es un modelo de visión artificial utilizado para la detección de objetos en imágenes y videos. Su funcionamiento permite identificar diferentes objetos dentro de una imagen y determinar su ubicación mediante cuadros delimitadores (<i>bounding boxes</i>).
</p>

<p>
En este proyecto, YOLO se utilizó para identificar dos tipos de objetos: <b>motos</b> y <b>carros</b>. Dependiendo del objeto detectado, se envía una orden a la ESP32 para controlar los LEDs correspondientes.
</p>

<h2><b>Funcionamiento con la ESP32</b></h2>

<p>
La ESP32 se utiliza como dispositivo encargado de recibir las órdenes generadas por el programa de Python. De acuerdo con el objeto detectado por YOLO, la ESP32 puede encender el LED correspondiente.
</p>

<p>
El código utilizado en la ESP32 fue desarrollado en <b>MicroPython</b>. A continuación se deja el espacio para agregar el código utilizado:
</p>

<h3><b>Código de la ESP32</b></h3>

<pre>
<code>
from machine import Pin
import sys
import uselect
import time

# LEDS
rojo = Pin(26, Pin.OUT)
verde = Pin(27, Pin.OUT)

# ESTADO YOLO
deteccion_yolo = ""

# SERIAL
poll = uselect.poll()
poll.register(sys.stdin, uselect.POLLIN)

print("================================")
print("ESP32 LISTO (Solo YOLO, sin pulsadores)")
print("GPIO 27 -> LED VERDE (Moto)")
print("GPIO 26 -> LED ROJO (Carro)")
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

    # CONTROL DE LEDS SEGÚN YOLO
    if deteccion_yolo == "CARRO":
        rojo.value(1)
        verde.value(0)

    elif deteccion_yolo == "MOTO":
        rojo.value(0)
        verde.value(1)

    else:
        # Si recibe "NINGUNO" o está vacío, apaga ambos
        rojo.value(0)
        verde.value(0)

    time.sleep_ms(10)
</code>
</pre>

<h2><b>Obtención del conjunto de datos</b></h2>

<p>
Para realizar el proyecto se utilizó <b>Roboflow</b>, una plataforma que permitió obtener un conjunto de datos ya organizado y preparado para el entrenamiento del modelo de detección de objetos.
</p>

<p>
El archivo obtenido contenía las imágenes y los datos correspondientes a dos clases de objetos: <b>carros de juguete</b> y <b>motos de juguete</b>. De esta manera, no fue necesario crear y organizar manualmente el conjunto de datos desde cero.
</p>

<p>
El conjunto de datos estuvo compuesto por:
</p>

<ul>
  <li><b>1498 imágenes de motos de juguete.</b></li>
  <li><b>1096 imágenes de carros de juguete.</b></li>
</ul>

<p>
Estas imágenes y sus respectivos datos fueron utilizados posteriormente para entrenar el modelo YOLO, permitiendo que este aprendiera a diferenciar entre un carro de juguete y una moto de juguete.
</p>

<p>
El conjunto de datos fue obtenido mediante la plataforma 
<a href="https://roboflow.com/"><b>Roboflow</b></a>.
</p>

<h3><b>Conjunto de datos utilizado</b></h3>

<p align="center">
  <img src="Imagenes/YOLO/Roboflow.png" alt="Conjunto de datos utilizado en Roboflow" width="700">
</p>

<h2><b>Entrenamiento del modelo</b></h2>

<p>
Después de obtener el conjunto de datos desde <b>Roboflow</b>, se procedió a entrenar el modelo de <b>YOLO</b> para que pudiera reconocer las dos clases de objetos: <b>moto de juguete</b> y <b>carro de juguete</b>.
</p>

<p>
Para realizar el entrenamiento se utilizó <b>Google Colab</b>, debido a que el entrenamiento de un modelo de visión artificial requiere una mayor capacidad de procesamiento. Esta herramienta permitió utilizar recursos computacionales adecuados para realizar el entrenamiento del modelo.
</p>
<p>
En Google Colab se ingresaron los archivos correspondientes al conjunto de datos obtenido desde Roboflow y posteriormente se ejecutó el proceso de entrenamiento del modelo.
</p>

<h3><b>Proceso de entrenamiento</b></h3>

<p align="center">
  <!-- Colocar aquí la imagen del proceso de entrenamiento en Google Colab -->
  <img src="Imagenes/YOLO/Entrenamiento.png" alt="Entrenamiento del modelo YOLO en Google Colab" width="700">
</p>

<h3><b>Código utilizado para el entrenamiento</b></h3>

<pre>
<code>
# =========================================================
# CÓDIGO DE ENTRENAMIENTO EN GOOGLE COLAB
# =========================================================

# Pegar aquí el código utilizado para entrenar YOLO.
</code>
</pre>

<h2><b>Modelo generado</b></h2>

<p>
Una vez finalizado el entrenamiento, Google Colab generó el modelo entrenado, el cual posteriormente fue utilizado para realizar la detección de motos y carros.
</p>

<p>
Este modelo permite analizar las imágenes capturadas por la cámara y determinar qué objeto se encuentra presente.
</p>

<h2><b>Programa principal en Python</b></h2>

<p>
Después de entrenar el modelo, se desarrolló un programa en <b>Python</b> encargado de utilizar YOLO para realizar la detección de objetos y comunicarse con la ESP32.
</p>

<p>
El programa recibe la imagen de la cámara, ejecuta el modelo YOLO y determina si el objeto detectado corresponde a una <b>moto</b> o a un <b>carro</b>. Posteriormente, de acuerdo con el resultado de la detección, se envía la orden correspondiente a la ESP32.
</p>

<h3><b>Código principal de Python</b></h3>

<pre>
<code>
# =========================================================
# CÓDIGO PRINCIPAL EN PYTHON
# =========================================================

# Pegar aquí el código principal de Python.
</code>
</pre>

<h2><b>Funcionamiento del sistema</b></h2>

<p>
El funcionamiento completo del sistema se puede resumir de la siguiente manera:
</p>

<ol>
  <li>Se obtiene una imagen mediante la cámara.</li>
  <li>El programa de Python procesa la imagen.</li>
  <li>YOLO analiza la imagen y busca los objetos entrenados.</li>
  <li>El modelo identifica si el objeto corresponde a una moto o a un carro.</li>
  <li>Python genera la orden correspondiente.</li>
  <li>La orden es enviada a la ESP32.</li>
  <li>La ESP32 recibe la orden y controla el LED correspondiente.</li>
</ol>

<p align="center">
  <img src="Imagenes/YOLO/Funcionamiento.png" alt="Funcionamiento del sistema YOLO y ESP32" width="700">
</p>

<h2><b>Video de funcionamiento</b></h2>

<p>
A continuación se encuentra el enlace al video donde se puede observar el funcionamiento completo del sistema, incluyendo la detección de los objetos mediante YOLO y la respuesta de la ESP32.
</p>

<p align="center">
  <a href="https://www.youtube.com/" target="_blank">
    <b>Ver video de funcionamiento en YouTube</b>
  </a>
</p>

<p>
<i>El enlace será actualizado posteriormente con el video correspondiente.</i>
</p>

