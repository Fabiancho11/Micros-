import serial
import requests
import time


# ==================================================
# CONFIGURACIÓN
# ==================================================

# Pon aquí tu API Key COMPLETA de DeepSeek
API_KEY = "sk-b4357f4022f444a98d2ae4b60a7c6e5a"

# CAMBIA COM3 por el puerto de tu ESP32
PUERTO = "COM3"

BAUDRATE = 115200


# ==================================================
# CONECTAR CON ESP32
# ==================================================

try:

    esp32 = serial.Serial(
        PUERTO,
        BAUDRATE,
        timeout=2
    )

    time.sleep(2)

    print("ESP32 conectada correctamente")
    print("Puerto:", PUERTO)

except Exception as e:

    print("ERROR conectando con la ESP32")
    print(e)

    exit()


# ==================================================
# ENVIAR COMANDO A ESP32
# ==================================================

def enviar_comando(comando):

    try:

        esp32.write((comando + "\n").encode())

        respuesta = esp32.readline().decode().strip()

        return respuesta

    except Exception as e:

        return "Error de comunicación: " + str(e)


# ==================================================
# INTERPRETAR ORDEN DE LED
# ==================================================

def controlar_led(mensaje):

    texto = mensaje.lower()

    # -------------------------
    # ROJO
    # -------------------------

    if "rojo" in texto:

        if "enciende" in texto or "encender" in texto:
            return enviar_comando("ROJO_ON")

        if "apaga" in texto or "apagar" in texto:
            return enviar_comando("ROJO_OFF")


    # -------------------------
    # VERDE
    # -------------------------

    if "verde" in texto:

        if "enciende" in texto or "encender" in texto:
            return enviar_comando("VERDE_ON")

        if "apaga" in texto or "apagar" in texto:
            return enviar_comando("VERDE_OFF")


    # -------------------------
    # TODOS
    # -------------------------

    if "todos" in texto:

        if "enciende" in texto or "encender" in texto:
            return enviar_comando("TODOS_ON")

        if "apaga" in texto or "apagar" in texto:
            return enviar_comando("TODOS_OFF")


    return None


# ==================================================
# DEEPSEEK
# ==================================================

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


# ==================================================
# CHATBOT
# ==================================================

print()
print("==========================================")
print("       CHATBOT DEEPSEEK + ESP32")
print("==========================================")
print()
print("Puedes decir:")
print()
print("  enciende el rojo")
print("  apaga el rojo")
print("  enciende el verde")
print("  apaga el verde")
print("  enciende todos")
print("  apaga todos")
print()
print("También puedes hacer preguntas a DeepSeek.")
print("Escribe 'salir' para terminar.")
print()


while True:

    mensaje = input("Tú: ")

    # SALIR
    if mensaje.lower() == "salir":

        print("Chatbot: Hasta luego!")

        break


    # ==========================================
    # PRIMERO: COMPROBAR SI ES ORDEN DE LED
    # ==========================================

    resultado = controlar_led(mensaje)


    if resultado is not None:

        print("ESP32:", resultado)


    # ==========================================
    # SI NO ES LED → DEEPSEEK
    # ==========================================

    else:

        respuesta = hablar_con_deepseek(mensaje)

        print()
        print("Chatbot:", respuesta)
        print()