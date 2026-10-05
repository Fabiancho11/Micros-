<p><strong>Integrantes:</strong></p>

<ul>
    <li>Jeicob David Pinilla Ruiz</li>
    <li>Fabian Abril Casallas</li>
</ul>

<h1><b>PUNTO 1</b></h1>

<p>
Por medio de un teclado matricial se ingresa un numero de 0-9 
el cual se visualiza en una LCD 16X2 controlada por una ESP 32 
que envia el numero por medio del puerto serial al computador 
para que se visualice el como el brazo dibuja el numero en Pybullet.
</p>

<h2><b>Python 3.11</b></h2>

<p>
Para poder usar Pybullet en pyton fue necesario utilizar la version
<strong>3.11</strong> de pyton ya que esta version tiene mayor compatibilidad
con Pybullet.
</p>

<pre><code># Creación y activación del entorno virtual en Windows

python3.11 -m venv venv
venv\Scripts\activate

# Instalación de las librerías necesarias

pip install pybullet pyserial
</code></pre>

<p>
Como ya tenia instalado <strong>Pyton 3.14</strong> fue necesario 
descargar <strong>Pyton 3.11</strong> y activarlo en entorno virtual
para poder alternar entre ambas versiones y no estar instalando y
desinstalando cada version.
</p>

<h2><b>Funcionamiento</b></h2>

<h3><b>1. Captura de datos mediante MicroPython</b></h3>

<p>
La ESP32 lee constantemente el teclado. Cuando se presiona un
boton, el programa aplica un filtro antirrebote para evitar lecturas duplicadas.
Posteriormente muestra la tecla presionada en la pantalla LCD y envía el número
a la computadora mediante el puerto serial.
</p>

<h3><b>2. Recepción de datos en el computador</b></h3>

<p>
Un programa desarrollado en Python recibe los datos enviados 
por la ESP32, Cuando recibe un número válido entre 0 y 9 
manda la orden para dibujar el numero.
</p>

<h3><b>3. Dibujo del numero</b></h3>

<p>
El programa contiene las instrucciones geométricas necesarias para representar
cada número. Los puntos correspondientes al numero son ajustados al tamaño
adecuado y posteriormente rotados para que el número quede orientado.
</p>

<h3><b>4. Movimiento del brazo y dibujo 3D</b></h3>

<p>
El motor de simulación calcula las posiciones necesarias de las articulaciones
del brazo para alcanzar cada punto. A medida que la punta del brazo se desplaza 
se genera un rastro que representa el dibujo.
Cuando el número contiene partes separadas, como ocurre con algunos trazos del
número 4, el brazo levanta el lápiz antes de desplazarse hacia la siguiente
posición.
</p>

<h2><b>Diagrama de bloques</b></h2>

<p align="center">
    <!-- Colocar aquí la imagen del diagrama de bloques -->
    <img src="../Imagenes/bloque2.png"
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
Mediante openCV y comuniacion SPI se detecta un numero dibujado
el cual se envia por medio del protocolo de comunicacion ESP NOW
entre dos ESP una maestro y otra esclavo de tal manera que una
esta conectada al computador y reconoce el numero 
y se lo envia a la otra para que lo muestre en una pantalla OLED.
</p>

<h2><b>2. Diagrama de Bloques</b></h2>

<p align="center">
    <img src="../Imagenes/bloque3.png"
         alt="Diagrama de bloques del sistema"
         width="900">
</p>

<h2><b>3. Funcionamiento </b></h2>

<h3><b>Código 1: Reconocimiento con Python y OpenCV</b></h3>

<p>
Este programa se ejecuta en el computador utilizando una cámara para el reconocimeinto. 
Utiliza la biblioteca <strong>OpenCV</strong> para capturar el video en tiempo real.
</p>

<p>
Posteriormente, la imagen es procesada mediante conversión a escala de grises
con el objetivo de aislar los trazos escritos a mano o impresos. 
Mediante la función <code>reconocer_numero()</code>, el programa
analiza las características del contorno y determina el número de agujeros
presentes en el dígito.
</p>

<p>
Además se utiliza la transformada de distancia de Chamfer para comparar la
imagen capturada con diferentes plantillas previamente definidas. Cuando se
identifica un dígito del 0 al 9 con un nivel de confianza adecuado, el número
es enviado mediante el puerto serial <code>COM10</code> al primer
microcontrolador.
</p>

<h3><b>Código 2: Maestro (ESP-A)</b></h3>

<p>
Este programa se ejecuta en la ESP maestro, llamada
<strong>ESP-A</strong>. Su función principal es comunicar
de manera inalambrica el computador y la segunda ESP.
</p>

<ul>
    <li>
        Configura el protocolo <strong>ESP-NOW</strong> y registra la dirección
        MAC del dispositivo receptor.
    </li>
    <li>
        Lee los datos provenientes del computador mediante la comunicación
        serial.
    </li>
    <li>
        Detecta el salto de línea que indica el final del mensaje recibido.
    </li>
    <li>
        Envía el número recibido de forma inalámbrica mediante ESP-NOW hacia
        el ESP32-S3.
    </li>
</ul>

<h3><b>Código 3: Esclavo (ESP32-S3)</b></h3>

<p>
Este programa se ejecuta en una <strong>ESP32-S3</strong> que funciona como
la ESP que recibe el numero y lo muestra.
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
        Cuando recibe un mensaje válido, muestra el número recibido.
    </li>
    <li>
        Finalmente actualiza la pantalla OLED para mostrar el número
        reconocido en el centro de la pantalla.
    </li>
</ul>

<p align="center">
    <a href="https://youtu.be/kkkakf-kYo8" target="_blank">
        <b>Video de funcionamiento</b>
    </a>
</p>
