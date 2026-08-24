<h1>Primer Parcial - Microcontroladores - Auto</h1>

<p><strong>Integrantes:</strong></p>
<ul>
    <li>Jeicob David Pinilla Ruiz</li>
    <li>Fabian Abril Casallas</li>
</ul>

<h2>Simulación en Wokwi</h2>

<p>
    Antes de realizar la implementación física, el proyecto fue simulado en
    Wokwi. La simulación permitió comprobar el funcionamiento del código y
    verificar la correcta generacion del auto por medio de la ESP-32.
</p>

<!-- Imagen de la simulación -->
<img src="../Imagenes/Simulacion.jpg" alt="Simulación del auto en Wokwi">

<p>
    <strong>Enlace de la simulación:</strong>
    <a href="https://wokwi.com/projects/472703213305188353" target="_blank">
        Ver simulación en Wokwi
    </a>
</p>

<hr>

<h1>Auto</h1>

<p>
    Este proyecto muestra cómo usar un microcontrolador, como el ESP32, para dibujar la
    silueta de un auto en la pantalla de un osciloscopio clásico. Para lograrlo, se utilizan
    los pines DAC (Convertidor Digital a Analógico) y se configura el osciloscopio en
    <strong>modo X-Y</strong>.
</p>

<h2>¿Cómo se hace la figura paso a paso?</h2>

<p>
    Dibujar en un osciloscopio no es como imprimir una imagen. Se utiliza un punto de luz
    que debe moverse constantemente por la pantalla para formar la figura.
</p>

<h3>1. Controlando el rayo de luz: los DAC</h3>

<p>
    Los pines 25 y 26 del ESP32 cuentan con conversión digital a analógica. Esto permite
    generar diferentes niveles de voltaje en lugar de simplemente tener un estado de
    encendido o apagado.
</p>

<ul>
    <li><strong>GPIO 25:</strong> controla el movimiento horizontal, correspondiente al eje X.</li>
    <li><strong>GPIO 26:</strong> controla el movimiento vertical, correspondiente al eje Y.</li>
</ul>

<p>
    Al cambiar los voltajes de ambos pines simultáneamente, es posible mover el punto de luz
    del osciloscopio a diferentes posiciones de la pantalla.
</p>

<h3>2. Creación de la silueta del auto</h3>

<p>
    El osciloscopio mantiene el rayo de luz encendido, por lo que no es posible levantar el
    lápiz como se haría al dibujar sobre papel. Por esta razón, el código utiliza una lista
    llamada <code>puntos_clave</code>, la cual contiene las coordenadas necesarias para
    formar la figura del auto mediante un recorrido continuo.
</p>

<p>
    El recorrido permite dibujar el chasis, las ruedas y otros elementos de la silueta,
    evitando saltos innecesarios entre las diferentes partes de la figura.
</p>

<h3>3. Interpolación de puntos</h3>

<p>
    Si únicamente se enviaran las coordenadas de las esquinas, el punto de luz realizaría
    saltos muy rápidos entre ellas. Para evitar esto, se utiliza la variable
    <code>pasos_por_linea = 20</code>.
</p>

<p>
    Mediante un ciclo <code>for</code> se generan puntos intermedios entre cada par de
    coordenadas. Esto permite que el punto de luz se desplace gradualmente y forme líneas
    más sólidas y definidas.
</p>

<h3>4. Actualización continua de la imagen</h3>

<p>
    El código utiliza un ciclo <code>while True</code> para repetir constantemente el
    recorrido de las coordenadas almacenadas en <code>ruta_x</code> y
    <code>ruta_y</code>.
</p>

<p>
    Debido a la persistencia de la visión y al refresco continuo de la pantalla, el ojo
    humano percibe una imagen fija, aunque en realidad el punto de luz está recorriendo
    continuamente toda la silueta del auto.
</p>

<h2>Código Completo</h2>

<pre><code>

from machine import DAC, Pin

# Configuramos los DAC en los pines 25 y 26
dac_x = DAC(Pin(25)) # Eje X (Canal 1)
dac_y = DAC(Pin(26)) # Eje Y (Canal 2)

# Coordenadas rediseñadas para un solo trazo continuo
# Coordenadas rediseñadas con llantas y ventana (Un solo trazo continuo)
puntos_clave = [
    # --- CARROCERÍA EXTERIOR ---
    (20, 50),   # Parachoques trasero (abajo)
    (20, 90),   # Parachoques trasero (arriba)
    (45, 90),   # Baúl
    (75, 140),  # Techo (atrás)
    (135, 140), # Techo (frente)
    (165, 90),  # Capó
    (220, 90),  # Parachoques delantero (arriba)
    (220, 50),  # Parachoques delantero (abajo)

    # --- RUEDA DELANTERA (Dibujada hacia abajo y afuera) ---
    (180, 50),  # Inicio guardabarros
    (180, 20),  # Llanta (baja)
    (140, 20),  # Llanta (fondo)
    (140, 50),  # Fin guardabarros

    (80, 50),   # Chasis inferior medio

    # --- RUEDA TRASERA ---
    (80, 20),   # Llanta (baja)
    (40, 20),   # Llanta (fondo)
    (40, 50),   # Fin guardabarros

    (20, 50),   # Vuelta al origen (Cierra el chasis inferior)

    # --- TRUCO PARA LA VENTANA (Entrar, dibujar y salir por el mismo camino) ---
    (20, 90),   # Retrazamos hacia arriba por el parachoques
    (45, 90),   # Retrazamos el baúl
    (55, 95),   # Entramos al interior del auto
    (125, 95),  # Base de la ventana
    (120, 130), # Frente de la ventana
    (70, 130),  # Techo de la ventana
    (55, 95),   # Cerramos la ventana
    (45, 90)    # Salimos de vuelta al baúl (Para reiniciar el ciclo limpiamente)
]
# Listas para almacenar el trazo completo
ruta_x = []
ruta_y = []

# Resolución: cuántos puntos intermedios calculamos por cada línea recta
pasos_por_linea = 20 

# Generamos la interpolación (el recorrido suave entre puntos)
for i in range(len(puntos_clave)):
    p1 = puntos_clave[i]
    p2 = puntos_clave[(i + 1) % len(puntos_clave)]
    
    for paso in range(pasos_por_linea):
        t = paso / pasos_por_linea
        x = int(p1[0] + (p2[0] - p1[0]) * t)
        y = int(p1[1] + (p2[1] - p1[1]) * t)
        ruta_x.append(x)
        ruta_y.append(y)

# Bucle infinito para refrescar el osciloscopio
while True:
    for i in range(len(ruta_x)):
        dac_x.write(ruta_x[i])
        dac_y.write(ruta_y[i])  

</code></pre>

<h2>Demostración en Video</h2>
<p>Mira el resultado final funcionando directamente en un osciloscopio real:</p>
<p><a href="https://youtube.com/shorts/MMPqPZSSY4s" target="_blank">Ver video de funcionamiento en YouTube</a></p>
