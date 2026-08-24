<h1>Auto </h1>

<p>Este proyecto muestra cómo usar un microcontrolador (como un ESP32) para dibujar la silueta de un auto en la pantalla de un osciloscopio clásico. Para lograrlo, usamos los pines DAC (Convertidor Digital a Analógico) y configuramos el osciloscopio en el famoso <strong>modo X-Y</strong>.</p>

<h2>¿Cómo se hace la figura paso a paso?</h2>

<p>Dibujar en un osciloscopio no es como imprimir una imagen; es más bien como jugar con un <em>Telesketch (Etch A Sketch)</em> súper rápido. Solo tienes un punto de luz que debes mover constantemente. Aquí te explico cómo funciona el código:</p>

<h3>1. Controlando el rayo de luz (Los DAC)</h3>
<p>Las primeras líneas del código configuran los pines 25 y 26. Estos pines tienen un DAC, lo que significa que pueden sacar un voltaje variable (analógico) en lugar de solo encendido/apagado (digital). El pin 25 controla el movimiento horizontal (Eje X) y el pin 26 controla el vertical (Eje Y). Al variar los voltajes al mismo tiempo, movemos el punto de luz a cualquier coordenada de la pantalla.</p>

<h3>2. El problema de "no poder levantar el lápiz"</h3>
<p>El reto más grande en un osciloscopio es que el rayo de luz siempre está encendido. Si quieres dibujar el contorno del auto y luego una ventana, no puedes "levantar el lápiz" para saltar al centro. ¿La solución? El código define una lista de <code>puntos_clave</code> que traza el carro en <strong>un solo trazo continuo</strong>. Empieza por el chasis, hace las llantas hacia abajo y vuelve a subir. Para hacer la ventana, el trazo entra por el baúl, dibuja el cuadrado de la ventana, y <em>se devuelve por el mismo camino</em> para salir de nuevo al contorno sin que se note una línea extra cruzando el auto.</p>

<h3>3. Rellenando los huecos (Interpolación)</h3>
<p>Si solo le enviamos al osciloscopio las coordenadas de las esquinas (los puntos clave), el punto de luz saltaría tan rápido de un extremo a otro que apenas veríamos unas líneas muy tenues o el dibujo se deformaría. Por eso usamos la variable <code>pasos_por_linea = 20</code>. El ciclo <code>for</code> que le sigue hace un cálculo matemático simple para crear 20 puntos intermedios entre cada esquina. Esto obliga al rayo del osciloscopio a viajar más despacio y dibujar líneas sólidas y bien definidas.</p>

<h3>4. Engañando al ojo humano (El bucle infinito)</h3>
<p>Al final del código hay un <code>while True</code>. El fósforo de la pantalla del osciloscopio brilla solo por una fracción de segundo. Para que veamos un auto completo y estático, el microcontrolador tiene que enviar todas las coordenadas (la lista <code>ruta_x</code> y <code>ruta_y</code>) una y otra vez lo más rápido posible. Gracias a la persistencia de nuestra visión, en lugar de ver un punto moviéndose a toda velocidad, vemos la imagen fija del coche.</p>


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

<h2>Simulación</h2>
<p>Puedes probar este circuito y ver cómo se dibuja paso a paso sin necesidad de hardware físico usando Wokwi.</p>
<p><strong>Enlace a la simulación en Wokwi:</strong> <a href="[https://wokwi.com/projects/472703213305188353]">[AQUÍ_PONES_TU_ENLACE_DE_WOKWI]</a></p>

<h2>Demostración en Video</h2>
<p>Mira el resultado final funcionando directamente en un osciloscopio real:</p>
<p><a href="https://youtube.com/shorts/MMPqPZSSY4s" target="_blank">Ver video de funcionamiento en YouTube</a></p>
