
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
# =========================================================
# CÓDIGO MICROPYTHON - ESP32
# =========================================================

# Pegar aquí el código utilizado en la ESP32.
</code>
</pre>

<h2><b>Librerías utilizadas</b></h2>

<p>
Para desarrollar el sistema se utilizaron diferentes librerías de Python necesarias para la comunicación con la ESP32, procesamiento de imágenes, funcionamiento del modelo YOLO y ejecución del programa.
</p>

<p>
Las librerías utilizadas fueron descargadas e instaladas previamente en el entorno de desarrollo.
</p>

<pre>
<code>
# =========================================================
# LIBRERÍAS UTILIZADAS
# =========================================================

# Escribir aquí las librerías utilizadas en el proyecto.
</code>
</pre>

<h2><b>Obtención del conjunto de datos</b></h2>

<p>
Para entrenar el modelo se utilizó <b>Roboflow</b>, donde se obtuvo un conjunto de imágenes de los objetos que se querían detectar.
</p>

<p>
El conjunto de datos estuvo compuesto por:
</p>

<ul>
  <li><b>1498 imágenes de motos.</b></li>
  <li><b>1096 imágenes de carros.</b></li>
</ul>

<p>
Estas imágenes fueron utilizadas como datos de entrenamiento para que el modelo pudiera aprender a diferenciar entre una moto y un carro.
</p>

<h3><b>Conjunto de datos utilizado</b></h3>

<p align="center">
  <!-- Colocar aquí la imagen del conjunto de datos de Roboflow -->
  <img src="Imagenes/YOLO/Roboflow.png" alt="Conjunto de datos utilizado en Roboflow" width="700">
</p>

<h2><b>Entrenamiento del modelo</b></h2>

<p>
Después de obtener las imágenes, fue necesario entrenar el modelo de YOLO para que pudiera reconocer correctamente las dos clases: <b>moto</b> y <b>carro</b>.
</p>

<p>
Para realizar el entrenamiento se utilizó <b>Google Colab</b>, debido a que el entrenamiento de un modelo de visión artificial requiere una mayor capacidad de procesamiento. Colab permitió utilizar recursos computacionales superiores a los disponibles localmente.
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

