<p><strong>Integrantes:</strong></p>

<ul>
    <li>Jeicob David Pinilla Ruiz</li>
    <li>Fabian Abril Casallas</li>
</ul>

<h1><b>PUNTO 1</b></h1>

<p>
Sistema de dibujo 3D que integra un brazo robótico controlado mediante una ESP32
con una simulación virtual desarrollada en PyBullet. El sistema permite ingresar
un número mediante un teclado físico conectado a la ESP32 y posteriormente
enviar esta información a un computador mediante comunicación serial.
</p>

<h2><b>Requisito especial: Python 3.11</b></h2>

<p>
Para realizar la simulación en la computadora fue necesario utilizar
<strong>Python 3.11</strong>. Esta versión permite trabajar de manera estable
con las librerías utilizadas en el proyecto, especialmente PyBullet y PySerial.
</p>

<pre><code># Creación y activación del entorno virtual en Windows

python3.11 -m venv venv
venv\Scripts\activate

# Instalación de las librerías necesarias

pip install pybullet pyserial
</code></pre>

<h2><b>¿Cómo funciona el sistema?</b></h2>

<h3><b>1. Captura de datos mediante MicroPython</b></h3>

<p>
La placa ESP32 lee constantemente el teclado físico. Cuando se presiona un
botón, el programa aplica un filtro antirrebote para evitar lecturas duplicadas.
Posteriormente, muestra la tecla presionada en la pantalla LCD y envía el número
a la computadora mediante el cable USB.
</p>

<h3><b>2. Recepción de datos en el computador</b></h3>

<p>
Un programa desarrollado en Python permanece escuchando el puerto USB de la
ESP32. Cuando recibe un número válido entre 0 y 9, interpreta la información
y activa la orden correspondiente para comenzar el dibujo en el entorno virtual.
</p>

<h3><b>3. Generación de la forma</b></h3>

<p>
El programa contiene las instrucciones geométricas necesarias para representar
cada número. Los puntos correspondientes a la figura son ajustados al tamaño
adecuado y posteriormente rotados para que el número quede orientado
correctamente respecto a la cámara del simulador.
</p>

<h3><b>4. Movimiento del brazo y dibujo 3D</b></h3>

<p>
El motor de simulación calcula las posiciones necesarias de las articulaciones
del brazo para alcanzar cada punto mediante cinemática inversa. A medida que
la punta del brazo se desplaza, se genera un rastro que representa el dibujo.
Cuando el número contiene partes separadas, como ocurre con algunos trazos del
número 4, el brazo levanta el lápiz antes de desplazarse hacia la siguiente
posición.
</p>

<h2><b>Diagrama de bloques</b></h2>

<p align="center">
    <!-- Colocar aquí la imagen del diagrama de bloques -->
    <img src="../Imagenes/DiagramaBloques.png"
         alt="Diagrama de bloques del sistema"
         width="800">
</p>

<h2><b>Video de funcionamiento</b></h2>

<p align="center">
    <!-- Colocar aquí el enlace del video -->
    <a href="https://youtu.be/UvwNwgkJg9M" target="_blank">
        <b>Ver video de funcionamiento</b>
    </a>
</p>

<p align="center">

<h1><b>PUNTO 2</b></h1>

<p>
El sistema integra visión artificial, comunicación serial y comunicación inalámbrica
mediante ESP-NOW para reconocer números utilizando una cámara conectada a un
computador y posteriormente transmitir el resultado entre dos microcontroladores
ESP32. Finalmente, el número reconocido es mostrado en una pantalla OLED.
</p>

<h2><b>1. Demostración en Video</b></h2>

<p>
En el siguiente enlace se puede observar el funcionamiento completo del sistema,
desde el reconocimiento del número mediante la cámara hasta su visualización
en la pantalla OLED.
</p>

<p align="center">
    <!-- Colocar aquí el enlace del video -->
    <a href="https://youtu.be/kkkakf-kYo8" target="_blank">
        <b>Ver video de funcionamiento</b>
    </a>
</p>

<h2><b>2. Diagrama de Bloques</b></h2>

<p align="center">
    <img src="../Imagenes/DiagramaBloques.png"
         alt="Diagrama de bloques del sistema"
         width="900">
</p>

<p>
El funcionamiento general del sistema se puede representar mediante la siguiente
secuencia:
</p>

<ul>
    <li><strong>Cámara del PC:</strong> captura la imagen del número.</li>
    <li><strong>Python y OpenCV:</strong> procesa la imagen y reconoce el dígito.</li>
    <li><strong>ESP-A (Maestro):</strong> recibe el número mediante comunicación serial USB.</li>
    <li><strong>ESP32-S3 (Esclavo):</strong> recibe inalámbricamente el número mediante ESP-NOW.</li>
    <li><strong>Pantalla OLED:</strong> muestra el número reconocido.</li>
</ul>

<h2><b>3. Explicación de los Códigos</b></h2>

<h3><b>Código 1: Reconocimiento con Python y OpenCV</b></h3>

<p>
Este programa se ejecuta en un computador conectado a una cámara. Utiliza la
biblioteca <strong>OpenCV</strong> para capturar el video en tiempo real y
extraer una región de interés (ROI).
</p>

<p>
Posteriormente, la imagen es procesada mediante conversión a escala de grises
y binarización adaptativa con el objetivo de aislar los trazos escritos a mano
o impresos. Mediante la función <code>reconocer_numero()</code>, el programa
analiza las características del contorno y determina el número de agujeros
presentes en el dígito.
</p>

<p>
Además, se utiliza la transformada de distancia de Chamfer para comparar la
imagen capturada con diferentes plantillas previamente definidas. Cuando se
identifica un dígito del 0 al 9 con un nivel de confianza adecuado, el número
es enviado mediante el puerto serie <code>COM10</code> al primer
microcontrolador.
</p>

<h3><b>Código 2: Transmisor Maestro (ESP-A)</b></h3>

<p>
Este programa se ejecuta en el microcontrolador maestro, denominado
<strong>ESP-A</strong>. Su función principal es actuar como puente de
comunicación entre el computador y el segundo microcontrolador.
</p>

<ul>
    <li>
        Configura el protocolo <strong>ESP-NOW</strong> y registra la dirección
        MAC del dispositivo receptor.
    </li>
    <li>
        Lee los datos provenientes del computador mediante la comunicación
        serial USB.
    </li>
    <li>
        Detecta el salto de línea que indica el final del mensaje recibido.
    </li>
    <li>
        Envía el número recibido de forma inalámbrica mediante ESP-NOW hacia
        el ESP32-S3.
    </li>
</ul>

<h3><b>Código 3: Receptor Esclavo (ESP32-S3)</b></h3>

<p>
Este programa se ejecuta en un <strong>ESP32-S3</strong>, que funciona como
nodo esclavo o receptor del sistema.
</p>

<ul>
    <li>
        Inicializa el sistema y apaga el LED RGB integrado ubicado en el
        pin 48.
    </li>
    <li>
        Configura una pantalla OLED SSD1306 mediante comunicación I2C.
    </li>
    <li>
        Utiliza el pin 5 como SDA y el pin 6 como SCL para la comunicación I2C.
    </li>
    <li>
        Inicializa el protocolo ESP-NOW y permanece a la espera de mensajes
        provenientes del ESP-A.
    </li>
    <li>
        Cuando recibe un mensaje válido, decodifica el número recibido.
    </li>
    <li>
        Finalmente, actualiza la pantalla OLED para mostrar el número
        reconocido en el centro de la pantalla.
    </li>
</ul>

<h2><b>4. Evidencia del Funcionamiento</b></h2>

<p>
A continuación se puede colocar la evidencia fotográfica del sistema,
incluyendo la cámara utilizada para el reconocimiento, el ESP-A, el
ESP32-S3 y la pantalla OLED.
</p>

<p align="center">
    <img src="../Imagenes/Montaje.png"
         alt="Montaje del sistema de reconocimiento y comunicación ESP-NOW"
         width="800">
</p>

<h2><b>5. Flujo de Funcionamiento</b></h2>

<p>
El proceso completo comienza con la captura del número mediante la cámara.
Python procesa la imagen utilizando OpenCV y determina qué dígito fue
reconocido. El resultado se envía por comunicación serial al ESP-A.
Posteriormente, el ESP-A transmite el número de manera inalámbrica mediante
ESP-NOW al ESP32-S3. Finalmente, el ESP32-S3 recibe el dato y lo muestra
en la pantalla OLED.
</p>

<p align="center">
    <b>Cámara → Python/OpenCV → ESP-A → ESP-NOW → ESP32-S3 → OLED</b>
</p>
    <a href="https://youtu.be/EHqepvXtMkA" target="_blank">
        <b>Ver video de funcionamiento en YouTube</b>
    </a>
</p>
