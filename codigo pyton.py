import serial
import requests
import speech_recognition as sr
import sounddevice as sd
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import wave
import tempfile
import os

# CONFIGURACIÓN

API_KEY = "sk-b4357f4022f444a98d2ae4b60a7c6e5a"

PUERTO = "COM3"
BAUDRATE = 115200

# Configuración del micrófono

SAMPLE_RATE = 16000
CANALES = 1
DURACION = 5

# CONECTAR CON ESP32

try:

    esp32 = serial.Serial(
        PUERTO,
        BAUDRATE,
        timeout=2
    )

    time.sleep(2)

    conexion = True

except Exception as e:

    esp32 = None
    conexion = False

    print("ERROR conectando con la ESP32:")
    print(e)

# RECONOCEDOR

reconocedor = sr.Recognizer()

# ENVIAR COMANDO A ESP32

def enviar_comando(comando):

    if not conexion:
        return "ESP32 no conectada"

    try:

        esp32.write((comando + "\n").encode())

        respuesta = esp32.readline().decode(
            errors="ignore"
        ).strip()

        if respuesta == "":
            return "Comando enviado: " + comando

        return respuesta

    except Exception as e:

        return "Error de comunicación: " + str(e)

# INTERPRETAR ORDEN DE LED

def controlar_led(mensaje):

    texto = mensaje.lower().strip()

    # Palabras que significan ENCENDER
    
    encender = (
        "enciende" in texto
        or "encender" in texto
        or "prende" in texto
        or "prender" in texto
        or "activa" in texto
        or "activar" in texto
    )

    # Palabras que significan APAGAR
    
    apagar = (
        "apaga" in texto
        or "apagar" in texto
        or "desactiva" in texto
        or "desactivar" in texto
    )

    # TODOS

    if (
        "todos" in texto
        or "todas" in texto
        or "las dos" in texto
        or "ambos" in texto
        or "ambas" in texto
    ):

        if encender:
            return enviar_comando("TODOS_ON"), "TODOS_ON"

        if apagar:
            return enviar_comando("TODOS_OFF"), "TODOS_OFF"

    # ROJO

    if (
        "rojo" in texto
        or "roja" in texto
    ):

        if encender:
            return enviar_comando("ROJO_ON"), "ROJO_ON"

        if apagar:
            return enviar_comando("ROJO_OFF"), "ROJO_OFF"

    # VERDE

    if (
        "verde" in texto
        or "verde" in texto
    ):

        if encender:
            return enviar_comando("VERDE_ON"), "VERDE_ON"

        if apagar:
            return enviar_comando("VERDE_OFF"), "VERDE_OFF"


    return None, None

# DEEPSEEK

def hablar_con_deepseek(mensaje):

    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    datos = {

        "model": "deepseek-chat",

        "messages": [

            {
                "role": "system",
                "content":
                "Eres un asistente de inteligencia artificial. "
                "Responde en español de forma clara y sencilla."
            },

            {
                "role": "user",
                "content": mensaje
            }

        ]

    }

    try:

        respuesta = requests.post(
            url,
            headers=headers,
            json=datos,
            timeout=30
        )

        respuesta.raise_for_status()

        resultado = respuesta.json()

        return resultado["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as e:

        return f"Error de DeepSeek: {e}"

    except Exception as e:

        return f"Error inesperado: {e}"

# MOSTRAR EN EL CHAT

def mostrar(mensaje):

    chat.config(state=tk.NORMAL)

    chat.insert(
        tk.END,
        mensaje + "\n\n"
    )

    chat.see(tk.END)

    chat.config(state=tk.DISABLED)

# ACTUALIZAR ESTADO DE LOS LEDS

def actualizar_estado(comando):

    if comando == "ROJO_ON":

        estado_rojo.config(
            text="● ROJO: ENCENDIDO"
        )

    elif comando == "ROJO_OFF":

        estado_rojo.config(
            text="● ROJO: APAGADO"
        )

    elif comando == "VERDE_ON":

        estado_verde.config(
            text="● VERDE: ENCENDIDO"
        )

    elif comando == "VERDE_OFF":

        estado_verde.config(
            text="● VERDE: APAGADO"
        )

    elif comando == "TODOS_ON":

        estado_rojo.config(
            text="● ROJO: ENCENDIDO"
        )

        estado_verde.config(
            text="● VERDE: ENCENDIDO"
        )

    elif comando == "TODOS_OFF":

        estado_rojo.config(
            text="● ROJO: APAGADO"
        )

        estado_verde.config(
            text="● VERDE: APAGADO"
        )

# PROCESAR MENSAJE

def procesar_mensaje(mensaje):

    if not mensaje:
        return

    mostrar("Tú: " + mensaje)

    # COMPROBAR SI ES UNA ORDEN PARA LOS LEDS

    respuesta, comando = controlar_led(mensaje)

    if comando is not None:

        mostrar("ESP32: " + respuesta)

        actualizar_estado(comando)

        return


    # SI NO ES LED -> DEEPSEEK

    mostrar("DeepSeek: procesando...")

    respuesta = hablar_con_deepseek(mensaje)

    mostrar("DeepSeek: " + respuesta)

# GRABAR AUDIO CON SOUNDDEVICE

def grabar_audio():

    estado_voz.config(
        text="🎤 Escuchando..."
    )

    ventana.update_idletasks()

    try:

        # Grabar audio
        audio = sd.rec(
            int(DURACION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CANALES,
            dtype="int16"
        )

        sd.wait()

        estado_voz.config(
            text="Procesando voz..."
        )

        ventana.update_idletasks()

        # Crear archivo temporal WAV
        archivo_temporal = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        nombre_archivo = archivo_temporal.name

        archivo_temporal.close()

        # Guardar audio como WAV
        with wave.open(nombre_archivo, "wb") as archivo:

            archivo.setnchannels(CANALES)

            archivo.setsampwidth(2)

            archivo.setframerate(SAMPLE_RATE)

            archivo.writeframes(
                audio.tobytes()
            )


        # Abrir audio con SpeechRecognition
        with sr.AudioFile(nombre_archivo) as fuente:

            audio_sr = reconocedor.record(fuente)


        # Reconocer español
        texto = reconocedor.recognize_google(
            audio_sr,
            language="es-CO"
        )


        # Eliminar archivo temporal
        os.remove(nombre_archivo)


        # Mostrar texto reconocido
        entrada.delete(
            0,
            tk.END
        )

        entrada.insert(
            0,
            texto
        )


        # Procesar comando
        procesar_mensaje(texto)


    except sr.UnknownValueError:

        mostrar(
            "❌ No pude entender lo que dijiste."
        )

    except sr.RequestError as e:

        mostrar(
            "❌ Error del servicio de reconocimiento: "
            + str(e)
        )

    except Exception as e:

        mostrar(
            "❌ Error del micrófono: "
            + str(e)
        )


    estado_voz.config(
        text="Presiona HABLAR y da una orden"
    )

    boton_hablar.config(
        text="🎤 HABLAR",
        state=tk.NORMAL
    )

# INICIAR ESCUCHA

def iniciar_escucha():

    boton_hablar.config(
        text="🎤 ESCUCHANDO...",
        state=tk.DISABLED
    )

    hilo = threading.Thread(
        target=grabar_audio,
        daemon=True
    )

    hilo.start()

# ENVIAR TEXTO ESCRITO

def enviar_texto():

    mensaje = entrada.get().strip()

    if mensaje == "":
        return

    entrada.delete(
        0,
        tk.END
    )

    hilo = threading.Thread(
        target=procesar_mensaje,
        args=(mensaje,),
        daemon=True
    )

    hilo.start()

# BOTONES DIRECTOS

def comando_directo(comando, texto):

    respuesta = enviar_comando(comando)

    mostrar(
        "Sistema: " + texto
    )

    mostrar(
        "ESP32: " + respuesta
    )

    actualizar_estado(comando)

# VENTANA PRINCIPAL

ventana = tk.Tk()

ventana.title(
    "Asistente de Voz - ESP32"
)

ventana.geometry(
    "850x700"
)

ventana.resizable(
    False,
    False
)

# TÍTULO

titulo = tk.Label(
    ventana,
    text="🤖 ASISTENTE DE VOZ + ESP32",
    font=("Arial", 22, "bold")
)

titulo.pack(
    pady=15
)

# ESTADO ESP32

if conexion:

    texto_conexion = "● ESP32 CONECTADA"

else:

    texto_conexion = "● ESP32 DESCONECTADA"


estado_esp32 = tk.Label(
    ventana,
    text=texto_conexion,
    font=("Arial", 12, "bold")
)

estado_esp32.pack()

# ESTADO LEDS

marco_estados = tk.Frame(
    ventana
)

marco_estados.pack(
    pady=15
)


estado_rojo = tk.Label(
    marco_estados,
    text="● ROJO: APAGADO",
    font=("Arial", 14, "bold")
)

estado_rojo.grid(
    row=0,
    column=0,
    padx=40
)


estado_verde = tk.Label(
    marco_estados,
    text="● VERDE: APAGADO",
    font=("Arial", 14, "bold")
)

estado_verde.grid(
    row=0,
    column=1,
    padx=40
)

# BOTONES DE CONTROL

marco_botones = tk.Frame(
    ventana
)

marco_botones.pack(
    pady=5
)


tk.Button(
    marco_botones,
    text="🔴 Encender rojo",
    width=20,
    height=2,
    command=lambda: comando_directo(
        "ROJO_ON",
        "enciende el rojo"
    )
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


tk.Button(
    marco_botones,
    text="🔴 Apagar rojo",
    width=20,
    height=2,
    command=lambda: comando_directo(
        "ROJO_OFF",
        "apaga el rojo"
    )
).grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


tk.Button(
    marco_botones,
    text="🟢 Encender verde",
    width=20,
    height=2,
    command=lambda: comando_directo(
        "VERDE_ON",
        "enciende el verde"
    )
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


tk.Button(
    marco_botones,
    text="🟢 Apagar verde",
    width=20,
    height=2,
    command=lambda: comando_directo(
        "VERDE_OFF",
        "apaga el verde"
    )
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


tk.Button(
    marco_botones,
    text="💡 Encender todos",
    width=20,
    height=2,
    command=lambda: comando_directo(
        "TODOS_ON",
        "enciende todos"
    )
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)


tk.Button(
    marco_botones,
    text="💡 Apagar todos",
    width=20,
    height=2,
    command=lambda: comando_directo(
        "TODOS_OFF",
        "apaga todos"
    )
).grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)

# CHAT

chat = scrolledtext.ScrolledText(
    ventana,
    width=95,
    height=10,
    font=("Arial", 10),
    state=tk.DISABLED
)

chat.pack(
    pady=10
)

# ENTRADA DE TEXTO

marco_entrada = tk.Frame(
    ventana
)

marco_entrada.pack(
    pady=5
)


entrada = tk.Entry(
    marco_entrada,
    width=65,
    font=("Arial", 12)
)

entrada.grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    marco_entrada,
    text="Enviar",
    width=12,
    command=enviar_texto
).grid(
    row=0,
    column=1
)

# BOTÓN HABLAR

boton_hablar = tk.Button(
    ventana,
    text="🎤 HABLAR",
    font=("Arial", 16, "bold"),
    width=25,
    height=2,
    command=iniciar_escucha
)

boton_hablar.pack(
    pady=10
)


# ESTADO DEL MICRÓFONO

estado_voz = tk.Label(
    ventana,
    text="Presiona HABLAR y da una orden",
    font=("Arial", 10)
)

estado_voz.pack()

# MENSAJE INICIAL

mostrar(
    "Sistema iniciado.\n"
    "Ejemplos de comandos:\n"
    "• Enciende el rojo\n"
    "• Apaga el rojo\n"
    "• Prende el verde\n"
    "• Apaga la verde\n"
    "• Enciende todos\n"
    "• Apaga las dos luces"
)

# INICIAR INTERFAZ

ventana.mainloop()

# CERRAR ESP32

if esp32 is not None:

    if esp32.is_open:

        esp32.close()
