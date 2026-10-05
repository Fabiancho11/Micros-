<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot para controlar LEDs por voz</title>
    <style>
        /* Estilos generales para que se vea moderno y limpio */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f0f2f5; /* Fondo gris claro */
            color: #333;
        }

        /* Contenedor principal que centra todo en la pantalla */
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        /* Títulos */
        h1 {
            color: #1a5276;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h2 {
            color: #2980b9;
            margin-top: 40px;
            border-left: 4px solid #2980b9;
            padding-left: 10px;
        }
        h3 {
            color: #2c3e50;
        }

        /* Cuadro bonito para los integrantes */
        .integrantes {
            background-color: #e8f4f8;
            padding: 15px 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #bce8f1;
        }
        .integrantes p {
            margin: 0 0 10px 0;
            font-size: 1.1em;
            color: #31708f;
        }
        .integrantes ul {
            margin: 0;
            padding-left: 20px;
        }

        /* Diseño de los bloques de código (estilo editor oscuro) */
        pre {
            background-color: #272822;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto; /* Agrega barra de desplazamiento si el código es largo */
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }
        code {
            font-family: Consolas, "Courier New", monospace;
            font-size: 14px;
        }

        /* Estilos para centrar e integrar imágenes */
        .img-container {
            text-align: center;
            margin: 30px 0;
        }
        .img-container img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Botón de YouTube estilo profesional */
        .btn-youtube {
            display: block;
            width: fit-content;
            margin: 30px auto;
            padding: 15px 30px;
            background-color: #ff0000;
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 16px;
            border-radius: 5px;
            transition: background-color 0.3s ease;
            text-align: center;
        }
        .btn-youtube:hover {
            background-color: #cc0000;
        }
    </style>
</head>
<body>

    <div class="container">
        
        <div class="integrantes">
            <p><strong>Integrantes del Proyecto:</strong></p>
            <ul>
                <li>Jeicob David Pinilla Ruiz</li>
                <li>Fabian Abril Casallas</li>
            </ul>
        </div>

        <h1>CHATBOT PARA CONTROLAR LEDS POR VOZ</h1>

        <p>
            Para poder controlar el encendido y apagado de un LED rojo y un LED verde mediante comandos de voz utilizando un chatbot, se creó un sistema de control apoyado por el motor de inteligencia artificial Groq AI.
        </p>

        <h2>ESP32 MicroPython: Controla los LEDs y recibe comandos</h2>
        <p>Este es el código que va dentro de la tarjeta ESP32. Se encarga de leer los botones físicos y también de escuchar las órdenes que le envía la computadora por el cable USB.</p>

<pre><code>from machine import Pin
import sys
import select
import time

# =========================
# CONFIGURACIÓN DE LEDS
# =========================
rojo = Pin(26, Pin.OUT)
verde = Pin(27, Pin.OUT)

# Variables para guardar si el LED está prendido (1) o apagado (0)
estado_rojo = 0
estado_verde = 0

rojo.value(estado_rojo)
verde.value(estado_verde)

# =========================
# CONFIGURACIÓN PULSADORES
# =========================
pulsador_verde = Pin(12, Pin.IN, Pin.PULL_UP)
pulsador_rojo = Pin(14, Pin.IN, Pin.PULL_UP)

# Tiempos para evitar el "rebote" (que un pulso cuente doble)
ultimo_tiempo_v = 0
ultimo_tiempo_r = 0

# Configurar lectura del puerto serial sin bloquear el ciclo
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

print("ESP32 Lista y esperando comandos...")

while True:
    tiempo_actual = time.ticks_ms()

    # ==========================================
    # 1. CONTROL POR BOTONES FÍSICOS (Alternar)
    # ==========================================
    
    # Botón verde
    if pulsador_verde.value() == 0:
        if time.ticks_diff(tiempo_actual, ultimo_tiempo_v) > 300: # 300ms de espera
            estado_verde = not estado_verde # Alterna el estado
            verde.value(estado_verde)
            print("OK Verde", "Encendido" if estado_verde else "Apagado")
            ultimo_tiempo_v = tiempo_actual

    # Botón rojo
    if pulsador_rojo.value() == 0:
        if time.ticks_diff(tiempo_actual, ultimo_tiempo_r) > 300:
            estado_rojo = not estado_rojo
            rojo.value(estado_rojo)
            print("OK Rojo", "Encendido" if estado_rojo else "Apagado")
            ultimo_tiempo_r = tiempo_actual

    # ==========================================
    # 2. CONTROL POR SERIAL (Desde Python)
    # ==========================================
    eventos = poll_obj.poll(0)
    
    if eventos:
        comando = sys.stdin.readline().strip()
        
        if comando == "ROJO_ON":
            estado_rojo = 1
            rojo.value(estado_rojo)
            print("OK Rojo Encendido")
            
        elif comando == "ROJO_OFF":
            estado_rojo = 0
            rojo.value(estado_rojo)
            print("OK Rojo Apagado")
            
        elif comando == "VERDE_ON":
            estado_verde = 1
            verde.value(estado_verde)
            print("OK Verde Encendido")
            
        elif comando == "VERDE_OFF":
            estado_verde = 0
            verde.value(estado_verde)
            print("OK Verde Apagado")
            
        elif comando == "TODOS_ON":
            estado_rojo = 1
            estado_verde = 1
            rojo.value(estado_rojo)
            verde.value(estado_verde)
            print("OK Todos Encendidos")
            
        elif comando == "TODOS_OFF":
            estado_rojo = 0
            estado_verde = 0
            rojo.value(estado_rojo)
            verde.value(estado_verde)
            print("OK Todos Apagados")
</code></pre>

        <h2>Interfaz gráfica</h2>
        <p>
            La aplicación cuenta con una interfaz gráfica muy fácil de usar. Permite controlar los LEDs de tres maneras: manualmente tocando los botones, escribiendo órdenes de texto, o hablándole directamente al micrófono gracias a nuestro chatbot inteligente.
        </p>

        <div class="img-container">
            <!-- Asegúrate de que la ruta de tu imagen sea correcta -->
            <img src="../Imagenes/Interfaz.png" alt="Interfaz gráfica del sistema">
        </div>

        <h2>Código de la aplicación Python (PC)</h2>
        <p>
            Para darle "inteligencia" al sistema, usamos Groq AI. Funciona así: el programa escucha lo que dices o lees lo que escribes, se lo envía a la inteligencia artificial mediante una API, y la IA nos devuelve la orden exacta (en un formato llamado JSON). Finalmente, nuestro programa de Python le manda esa orden a la tarjeta ESP32 por el cable (puerto COM).
        </p>

        <h3>Código Python de la interfaz</h3>
<pre><code>import serial
import time
import speech_recognition as sr
from openai import OpenAI
import sounddevice as sd
import soundfile as sf
import os
import json
import tkinter as tk
import threading

# =========================================================
# 1. CONFIGURACIÓN
# =========================================================
PUERTO = 'COM3'
BAUDIOS = 115200
# =========================================================
# AQUI VA LA API KEY
# =========================================================
API_KEY = "API_KEY"

# =========================================================
# 2. CLASE DE LA INTERFAZ GRÁFICA
# =========================================================
class AppControlLED:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Control LEDs")
        self.root.geometry("450x300")  # Ventana más pequeña y compacta
        self.root.resizable(False, False)

        # Configurar cliente Groq
        self.cliente_ia = OpenAI(
            api_key=API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        self.conexion_serial = None
        
        self.crear_interfaz()
        self.conectar_serial()

    def conectar_serial(self):
        try:
            self.conexion_serial = serial.Serial(PUERTO, BAUDIOS, timeout=1)
            time.sleep(2)
            print(f"Microcontrolador conectado exitosamente en {PUERTO}")
        except serial.SerialException:
            print(f"Advertencia: No se pudo abrir {PUERTO}. Modo simulación activado.")

    def crear_interfaz(self):
        # --- SECCIÓN 1: Control Manual ---
        marco_manual = tk.LabelFrame(self.root, text="Control Manual", padx=10, pady=10)
        marco_manual.pack(padx=10, pady=10, fill="x")

        # Botones Rojos
        btn_rojo_on = tk.Button(marco_manual, text="Rojo ON", bg="#ffcccc", width=12, 
                                command=lambda: self.enviar_comando_directo("rojo_on"))
        btn_rojo_on.grid(row=0, column=0, padx=5, pady=5)

        btn_rojo_off = tk.Button(marco_manual, text="Rojo OFF", bg="#e6e6e6", width=12, 
                                 command=lambda: self.enviar_comando_directo("rojo_off"))
        btn_rojo_off.grid(row=0, column=1, padx=5, pady=5)

        # Botones Verdes
        btn_verde_on = tk.Button(marco_manual, text="Verde ON", bg="#ccffcc", width=12, 
                                 command=lambda: self.enviar_comando_directo("verde_on"))
        btn_verde_on.grid(row=1, column=0, padx=5, pady=5)

        btn_verde_off = tk.Button(marco_manual, text="Verde OFF", bg="#e6e6e6", width=12, 
                                  command=lambda: self.enviar_comando_directo("verde_off"))
        btn_verde_off.grid(row=1, column=1, padx=5, pady=5)

        # --- SECCIÓN 2: Control por Texto ---
        marco_texto = tk.LabelFrame(self.root, text="Orden por Texto", padx=10, pady=10)
        marco_texto.pack(padx=10, pady=5, fill="x")

        self.entrada_texto = tk.Entry(marco_texto, width=35)
        self.entrada_texto.pack(side="left", padx=5)

        btn_enviar_texto = tk.Button(marco_texto, text="Enviar", bg="#ccccff", 
                                     command=self.procesar_texto)
        btn_enviar_texto.pack(side="left", padx=5)

        # --- SECCIÓN 3: Control por Voz ---
        marco_voz = tk.LabelFrame(self.root, text="Orden por Voz", padx=10, pady=10)
        marco_voz.pack(padx=10, pady=5, fill="x")

        self.btn_voz = tk.Button(marco_voz, text="Hablar (4 seg)", bg="#ffccff", height=1, 
                                 command=self.procesar_voz)
        self.btn_voz.pack(fill="x", padx=5)

    # =========================================================
    # 3. LÓGICA DE LA APLICACIÓN
    # =========================================================

    def enviar_comando_directo(self, comando):
        """Envía comandos validados al microcontrolador."""
        if self.conexion_serial and self.conexion_serial.is_open:
            self.conexion_serial.write((comando + '\n').encode('utf-8'))
            print(f"ESP32: Enviado comando -> {comando}")
        else:
            print(f"Simulacion: {comando} (Puerto no conectado)")

    def interpretar_con_groq(self, texto_usuario):
        """Consulta a Groq para convertir lenguaje natural en comandos."""
        print("Chat Bot (Groq): Procesando la orden...")
        
        prompt = f"""
Analiza la siguiente orden en español para controlar dos LEDs.
Orden del usuario: "{texto_usuario}"
Los comandos posibles son únicamente:
- rojo_on
- rojo_off
- verde_on
- verde_off
Corrige automáticamente pequeños errores de escritura.
Devuelve los comandos correspondientes.
"""
        try:
            respuesta = self.cliente_ia.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}],
                reasoning_effort="low",
                max_completion_tokens=500,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "control_leds",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "comandos": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": ["rojo_on", "rojo_off", "verde_on", "verde_off"]
                                    }
                                }
                            },
                            "required": ["comandos"],
                            "additionalProperties": False
                        }
                    }
                }
            )

            contenido = respuesta.choices[0].message.content
            print("Chat Bot (Groq): Respuesta recibida con éxito.")
            
            if not contenido: return []
            
            datos = json.loads(contenido)
            return datos.get("comandos", [])

        except Exception as e:
            print(f"Error conectando con Groq: {e}")
            return []

    # =========================================================
    # 4. FUNCIONES MULTIHILO (Para no congelar la GUI)
    # =========================================================

    def procesar_texto(self):
        texto = self.entrada_texto.get().strip()
        if texto:
            print(f"\nTexto ingresado: '{texto}'")
            self.entrada_texto.delete(0, tk.END)
            threading.Thread(target=self.ejecutar_orden, args=(texto,), daemon=True).start()

    def procesar_voz(self):
        self.btn_voz.config(state="disabled", text="Grabando...", bg="#ff6666")
        threading.Thread(target=self.hilo_grabar_voz, daemon=True).start()

    def hilo_grabar_voz(self):
        duracion = 4
        frecuencia = 44100
        archivo_temp = "temporal.wav"

        print("\nEscuchando por 4 segundos...")
        
        try:
            grabacion = sd.rec(int(duracion * frecuencia), samplerate=frecuencia, channels=1)
            sd.wait()
            sf.write(archivo_temp, grabacion, frecuencia)
            
            reconocedor = sr.Recognizer()
            with sr.AudioFile(archivo_temp) as source:
                audio_data = reconocedor.record(source)
                texto = reconocedor.recognize_google(audio_data, language="es-ES")
                
            print(f"Dijiste: '{texto}'")
            self.ejecutar_orden(texto)

        except sr.UnknownValueError:
            print("No pude entender el audio.")
        except Exception as e:
            print(f"Error con el micrófono: {e}")
        finally:
            if os.path.exists(archivo_temp):
                os.remove(archivo_temp)
            
            self.root.after(0, lambda: self.btn_voz.config(state="normal", text="Hablar (4 seg)", bg="#ffccff"))

    def ejecutar_orden(self, texto):
        comandos = self.interpretar_con_groq(texto)
        if comandos:
            print(f"Chat Bot (Groq) determinó ejecutar: {', '.join(comandos)}")
            for cmd in comandos:
                self.enviar_comando_directo(cmd)
                time.sleep(0.1)
        else:
            print("No se identificaron comandos válidos.")

# =========================================================
# 5. INICIO DEL PROGRAMA
# =========================================================
if __name__ == "__main__":
    ventana = tk.Tk()
    app = AppControlLED(ventana)
    
    def al_cerrar():
        if app.conexion_serial and app.conexion_serial.is_open:
            app.conexion_serial.close()
            print("Puerto serie cerrado. Saliendo...")
        ventana.destroy()
        
    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)
    ventana.mainloop()
</code></pre>

        <h2>Diagrama de bloques</h2>
        <p>A continuación se muestra cómo se comunican todas las partes de nuestro proyecto:</p>
        <div class="img-container">
            <!-- Asegúrate de que la ruta de tu imagen sea correcta -->
            <img src="../Imagenes/DiagramaBloques.png" alt="Diagrama de bloques del sistema">
        </div>

        <h2>¡Mira cómo funciona! 🎥</h2>
        <p>Hicimos un video demostrando todo el sistema en acción. Puedes verlo haciendo clic en el siguiente botón:</p>
        
        <a href="https://youtu.be/EHqepvXtMkA" target="_blank" class="btn-youtube">
            ▶️ Ver video en YouTube
        </a>

    </div>

</body>
</html>
