<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control de Luces con Gestos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f4f4f9;
            color: #333;
        }
        h1, h2 {
            color: #2c3e50;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        pre {
            background-color: #272822;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 14px;
        }
        code {
            font-family: Consolas, "Courier New", monospace;
        }
        .video-link {
            display: inline-block;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #e74c3c;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .video-link:hover {
            background-color: #c0392b;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Controlando luces con las manos 👋💡</h1>
    
    <p>¡Hola a todos! Hoy quiero compartir con ustedes un proyecto súper divertido que armé. La idea principal es poder controlar unas luces LED usando solo gestos con mi mano. Para lograr esto, usé la cámara web de mi computadora y una placa llamada ESP32.</p>

    <h2>¿Qué hace este proyecto?</h2>
    <p>Como pueden ver en la imagen de referencia llamada <strong>image_9112e7.jpg</strong>, el sistema reconoce diferentes señas que hago con la mano y le dice a los LEDs cómo deben prenderse:</p>
    <ul>
        <li>✊ <strong>Puño cerrado:</strong> Prende el LED amarillo al 30% de fuerza.</li>
        <li>✌️ <strong>Signo de paz (dos dedos):</strong> Prende el LED azul al 70%.</li>
        <li>🖐️ <strong>Mano abierta:</strong> Prende el LED rojo al máximo (100%).</li>
        <li>👎 <strong>Pulgar abajo:</strong> Inicia una secuencia especial de luces (Modo 1).</li>
        <li>👍 <strong>Pulgar arriba:</strong> Inicia otra secuencia diferente (Modo 2).</li>
    </ul>

    <img src="image_9112e7.jpg" alt="Diagrama del proyecto con gestos y la placa ESP32">

    <h2>Demostración en Video 🎥</h2>
    <p>Para que vean que esto realmente funciona y no es magia, grabé un video donde muestro cómo muevo la mano y las luces cambian solas. Pueden verlo en YouTube haciendo clic en el botón de abajo:</p>
    
    <!-- Aquí puedes reemplazar "TU_ENLACE_AQUI" con el link real de tu video de YouTube -->
    <a href="TU_ENLACE_AQUI" class="video-link" target="_blank">Ver el video del funcionamiento en YouTube</a>

    <hr>

    <h2>1. El código de la computadora (Python) 🐍</h2>
    <p>Este es el primer programa. Funciona en mi computadora usando Python y una herramienta llamada MediaPipe. Básicamente, este código prende la cámara, mira mi mano, le dibuja unos puntitos imaginarios para saber qué dedos están levantados, y luego manda un número secreto (del 1 al 5) por un cable USB hacia la tarjeta ESP32.</p>

    <pre><code>
import cv2
import math
import time
import serial
import mediapipe as mp

# --- 1. CONFIGURACIÓN DE CÁMARA Y ESP32 ---
INDICE_CAMARA = 1  # Cambia por el índice de tu cámara/app
PUERTO_COM = 'COM3'
BAUD_RATE = 115200

# --- 2. CONFIGURACIÓN DE MEDIAPIPE ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --- 3. CONEXIÓN SERIAL CON ESP32 ---
try:
    esp32 = serial.Serial(PUERTO_COM, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    print(f"Conectado a la ESP32 en {PUERTO_COM}")
except Exception as e:
    print(f"Advertencia: No se pudo abrir {PUERTO_COM} ({e})")
    print("Modo de prueba: solo visualización.")
    esp32 = None

def detectar_gesto(landmarks):
    wrist = landmarks[0]
    thumb_tip = landmarks[4]
    thumb_mcp = landmarks[2]
    index_pip = landmarks[6]
    middle_mcp = landmarks[9]

    # Identificación de dedos levantados (Índice, Medio, Anular, Meñique)
    indice_arriba = landmarks[8].y < landmarks[6].y
    medio_arriba = landmarks[12].y < landmarks[10].y
    anular_arriba = landmarks[16].y < landmarks[14].y
    menique_arriba = landmarks[20].y < landmarks[18].y

    dedos_extendidos = sum([indice_arriba, medio_arriba, anular_arriba, menique_arriba])

    # Escala de la mano (distancia entre muñeca y nudillo medio)
    escala_mano = math.hypot(middle_mcp.x - wrist.x, middle_mcp.y - wrist.y)
    
    # Distancia entre la punta del pulgar y el lateral del índice (donde descansa en un puño)
    dist_pulgar_guardado = math.hypot(thumb_tip.x - index_pip.x, thumb_tip.y - index_pip.y)

    # 1. Victoria (Índice y Medio arriba) -> Comando '2'
    if indice_arriba and medio_arriba and not anular_arriba and not menique_arriba:
        return '2', "Victoria (Nivel 70%)"

    # 2. Palma Abierta (3 o 4 dedos extendidos) -> Comando '3'
    if dedos_extendidos >= 3:
        return '3', "Palma Abierta (Nivel 100%)"

    # 3. Gestos con los 4 dedos cerrados (Puño, Pulgar Arriba, Pulgar Abajo)
    if dedos_extendidos == 0:
        # Si la punta del pulgar está replegada sobre el índice = Puño Cerrado
        if dist_pulgar_guardado < (escala_mano * 0.40):
            return '1', "Puño (Nivel 30%)"

        # Si el pulgar se despega verticalmente:
        if thumb_tip.y < thumb_mcp.y:
            return '5', "Pulgar Arriba (Secuencia 2)"
        else:
            return '4', "Pulgar Abajo (Secuencia 1)"

    return None, "Gesto No Reconocido"

# --- 4. BUCLE DE CAPTURA Y TRANSMISIÓN ---
cap = cv2.VideoCapture(INDICE_CAMARA, cv2.CAP_DSHOW)
ultimo_comando = None
ultimo_envio = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    texto_gesto = "Esperando mano..."

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            comando, texto_gesto = detectar_gesto(hand_landmarks.landmark)

            # Envío de comando con filtro de tiempo (1 segundo entre repetidos)
            tiempo_actual = time.time()
            if comando and (comando != ultimo_comando or (tiempo_actual - ultimo_envio > 1.0)):
                if esp32 and esp32.is_open:
                    esp32.write(comando.encode())
                    print(f"Enviado a ESP32: '{comando}' -> {texto_gesto}")
                ultimo_comando = comando
                ultimo_envio = tiempo_actual

    # Interfaz visual
    cv2.putText(frame, f"Estado: {texto_gesto}", (10, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("Controlador de Gestos - ESP32", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if esp32 and esp32.is_open:
    esp32.close()
cv2.destroyAllWindows()
    </code></pre>

    <hr>

    <h2>2. El código de las luces (MicroPython para la ESP32) 💡</h2>
    <p>Este segundo código vive adentro de la tarjetita ESP32. Su trabajo es muy simple: todo el tiempo está escuchando por el cable USB. Cuando oye un número que le mandó la computadora, ajusta la energía que le manda a los LEDs (usando algo que los ingenieros llaman PWM, que es solo cambiar el brillo rápido) o hace las secuencias de encendido y apagado de las interrupciones.</p>

    <pre><code>
import sys
import time
import uselect
from machine import Pin, PWM

# =========================================================
# CONFIGURACIÓN PWM
# =========================================================

FREQ = 1000

led_30 = PWM(Pin(27), freq=FREQ, duty_u16=0)   # LED Amarillo
led_70 = PWM(Pin(26), freq=FREQ, duty_u16=0)   # LED Azul
led_100 = PWM(Pin(25), freq=FREQ, duty_u16=0)  # LED Rojo


# =========================================================
# FUNCIÓN PARA FIJAR BRILLO
# =========================================================

def fijar_brillo(led_pwm, porcentaje):
    duty = int((porcentaje / 100.0) * 65535)
    led_pwm.duty_u16(duty)


# =========================================================
# APAGAR TODOS
# =========================================================

def apagar_todos():
    fijar_brillo(led_30, 0)
    fijar_brillo(led_70, 0)
    fijar_brillo(led_100, 0)

apagar_todos()


# =========================================================
# MODO 1 - PULGAR ABAJO
#
# Amarillo -> Azul -> Rojo
# Luego apaga Rojo -> Azul -> Amarillo
# =========================================================

def ejecutar_modo1():
    # 1. Amarillo 30%
    fijar_brillo(led_30, 30)
    time.sleep(1)

    # 2. Azul 70%
    # Amarillo permanece encendido
    fijar_brillo(led_70, 70)
    time.sleep(1)

    # 3. Rojo 100%
    # Amarillo y Azul permanecen encendidos
    fijar_brillo(led_100, 100)
    time.sleep(1)

    # 4. Apagar Rojo
    fijar_brillo(led_100, 0)
    time.sleep(1)

    # 5. Apagar Azul
    fijar_brillo(led_70, 0)
    time.sleep(1)

    # 6. Apagar Amarillo
    fijar_brillo(led_30, 0)
    time.sleep(1)

    apagar_todos()


# =========================================================
# MODO 2 - PULGAR ARRIBA
#
# Rojo -> Azul -> Amarillo
# Luego apaga Amarillo -> Azul -> Rojo
# =========================================================

def ejecutar_modo2():
    # 1. Rojo 100%
    fijar_brillo(led_100, 100)
    time.sleep(1)

    # 2. Azul 70%
    # Rojo permanece encendido
    fijar_brillo(led_70, 70)
    time.sleep(1)

    # 3. Amarillo 30%
    # Rojo y Azul permanecen encendidos
    fijar_brillo(led_30, 30)
    time.sleep(1)

    # 4. Apagar Amarillo
    fijar_brillo(led_30, 0)
    time.sleep(1)

    # 5. Apagar Azul
    fijar_brillo(led_70, 0)
    time.sleep(1)

    # 6. Apagar Rojo
    fijar_brillo(led_100, 0)
    time.sleep(1)

    apagar_todos()


# =========================================================
# ESCUCHAR PUERTO USB SERIAL
# =========================================================

poll_obj = uselect.poll()
poll_obj.register(sys.stdin, uselect.POLLIN)

print("ESP32 lista en MicroPython (Modo PWM Activo)...")


# =========================================================
# BUCLE PRINCIPAL
# =========================================================

while True:
    if poll_obj.poll(10):
        comando = sys.stdin.read(1)

        if comando == "1":
            # Puño cerrado -> Amarillo 30%
            apagar_todos()
            fijar_brillo(led_30, 30)

        elif comando == "2":
            # Signo Victoria -> Azul 70%
            apagar_todos()
            fijar_brillo(led_70, 70)

        elif comando == "3":
            # Palma abierta -> Rojo 100%
            apagar_todos()
            fijar_brillo(led_100, 100)

        elif comando == "4":
            # Pulgar abajo
            ejecutar_modo1()

        elif comando == "5":
            # Pulgar arriba
            ejecutar_modo2()
    </code></pre>

    <p>¡Y eso es todo! Espero que les haya gustado este proyecto. Es súper fácil de hacer y muestra cómo podemos usar la tecnología para controlar cosas en el mundo real solo moviendo las manos.</p>
</div>

</body>
</html>
