<h1><b>CHATBOT DOMÓTICO PARA CONTROLAR LEDS POR VOZ</b></h1>

<p>
El proyecto consiste en controlar dos LEDs (rojo y verde) conectados a una ESP32
mediante comandos de voz, texto o botones en una interfaz gráfica.
</p>


<h2><b>1. Funcionamiento general</b></h2>

<p>
El sistema tiene tres partes principales:
</p>

<ul>
    <li><b>ESP32 (MicroPython):</b> controla los LEDs y recibe comandos.</li>

    <li><b>Aplicación en Python (GUI):</b> permite enviar comandos por botones,
    texto o voz.</li>

    <li><b>Chatbot (Groq AI):</b> interpreta el lenguaje natural y lo convierte
    en comandos simples.</li>
</ul>


<h3><b>Interfaz gráfica</b></h3>

<p>
La aplicación cuenta con una interfaz gráfica que permite controlar los LEDs
manualmente mediante botones, enviar órdenes mediante texto y utilizar
comandos de voz.
</p>

<p align="center">
    <!-- Colocar aquí la imagen de la interfaz gráfica -->
    <img src="../Imagenes/Interfaz.png"
         alt="Interfaz gráfica del sistema"
         width="700">
</p>


<h2><b>2. Diagrama de bloques</b></h2>

<p>
El usuario puede interactuar con el sistema mediante voz, texto o botones.
La aplicación Python recibe estas instrucciones, las procesa y envía los
comandos correspondientes a la ESP32. Finalmente, la ESP32 controla los
LEDs rojo y verde.
</p>

<p align="center">
    <!-- Colocar aquí la imagen del diagrama de bloques -->
    <img src="../Imagenes/DiagramaBloques.png"
         alt="Diagrama de bloques del sistema"
         width="800">
</p>


<h2><b>3. Código del ESP32 (MicroPython)</b></h2>

<p>
El código de la ESP32 fue desarrollado utilizando <b>MicroPython</b>.
El microcontrolador se encarga de recibir los comandos enviados desde
la aplicación y controlar el estado de los LEDs.
</p>

<h3><b>Código MicroPython</b></h3>

<pre>
<code>

<!--
AQUÍ COLOCAR EL CÓDIGO COMPLETO DEL ESP32 EN MICROPYTHON
-->

</code>
</pre>


<h2><b>4. Código de la aplicación Python (PC)</b></h2>

<p>
La aplicación desarrollada en <b>Python</b> permite controlar la ESP32
desde el computador mediante una interfaz gráfica. La aplicación permite
enviar comandos mediante botones, texto y voz.
</p>

<p>
Además, la aplicación utiliza el chatbot de <b>Groq AI</b> para interpretar
las instrucciones escritas o habladas por el usuario y convertirlas en
comandos que puede procesar la ESP32.
</p>

<h3><b>Código Python de la interfaz</b></h3>

<pre>
<code>

<!--
AQUÍ COLOCAR EL CÓDIGO COMPLETO DE LA INTERFAZ PYTHON
-->

</code>
</pre>


<h2><b>5. Conexión entre PC y ESP32</b></h2>

<p>
Para establecer la comunicación entre el computador y la ESP32 se deben
seguir los siguientes pasos:
</p>

<ol>

    <li>
        Conectar la ESP32 al PC mediante un cable USB.
    </li>

    <li>
        Identificar el puerto COM asignado a la ESP32.
    </li>

    <li>
        Configurar el puerto COM correspondiente en la aplicación Python.
    </li>

    <li>
        Ejecutar la aplicación Python.
    </li>

    <li>
        La aplicación enviará los comandos a la ESP32 mediante comunicación
        serial.
    </li>

</ol>


<h2><b>6. Diagrama de conexión (Hardware)</b></h2>

<p>
El sistema está compuesto por una ESP32, dos LEDs y dos pulsadores.
Cada LED se encuentra conectado a un GPIO de la ESP32 mediante una
resistencia de 220 Ω.
</p>

<p>
Las conexiones utilizadas son las siguientes:
</p>

<ul>

    <li><b>LED rojo:</b> GPIO 26.</li>

    <li><b>LED verde:</b> GPIO 27.</li>

    <li><b>Botón verde:</b> GPIO 12.</li>

    <li><b>Botón rojo:</b> GPIO 14.</li>

</ul>

<p align="center">
    <!-- Colocar aquí la imagen del diagrama de conexión -->
    <img src="../Imagenes/Conexion.png"
         alt="Diagrama de conexión del hardware"
         width="800">
</p>


<h2><b>7. Comandos disponibles</b></h2>

<table border="1" align="center" cellpadding="10" cellspacing="0">

    <tr>
        <th>COMANDO</th>
        <th>FUNCIÓN</th>
    </tr>

    <tr>
        <td>rojo_on</td>
        <td>Enciende el LED rojo</td>
    </tr>

    <tr>
        <td>rojo_off</td>
        <td>Apaga el LED rojo</td>
    </tr>

    <tr>
        <td>verde_on</td>
        <td>Enciende el LED verde</td>
    </tr>

    <tr>
        <td>verde_off</td>
        <td>Apaga el LED verde</td>
    </tr>

    <tr>
        <td>todos_on</td>
        <td>Enciende ambos LEDs</td>
    </tr>

    <tr>
        <td>todos_off</td>
        <td>Apaga ambos LEDs</td>
    </tr>

</table>


<h2><b>8. Funcionamiento del sistema</b></h2>

<p>
El sistema permite controlar los LEDs de diferentes maneras. El usuario
puede utilizar los botones físicos conectados a la ESP32, ingresar un
comando mediante texto o utilizar la entrada de voz desde la aplicación.
</p>

<p>
Cuando se utiliza voz o texto, la aplicación Python interpreta la orden
mediante el chatbot y genera el comando correspondiente. Este comando
es enviado por comunicación serial a la ESP32, que finalmente realiza
la acción solicitada sobre los LEDs.
</p>


<h2><b>Video de funcionamiento</b></h2>

<p>
A continuación se encuentra el enlace al video donde se puede observar
el funcionamiento completo del sistema, incluyendo el control de los
LEDs mediante la interfaz, texto y comandos de voz.
</p>

<p align="center">
    <!-- Cambiar el enlace por el video real -->
    <a href="https://www.youtube.com/" target="_blank">
        <b>Ver video de funcionamiento en YouTube</b>
    </a>
</p>
