from machine import Pin

# CONFIGURACIÓN DE LEDS

rojo = Pin(26, Pin.OUT)
verde = Pin(27, Pin.OUT)

# Apagar al iniciar
rojo.value(0)
verde.value(0)

print("ESP32 LISTA")
print("Esperando comandos...")

# RECIBIR COMANDOS

while True:

    comando = input().strip()

    # LED ROJO
    if comando == "ROJO_ON":
        rojo.value(1)
        print("LED ROJO ENCENDIDO")

    elif comando == "ROJO_OFF":
        rojo.value(0)
        print("LED ROJO APAGADO")

    # LED VERDE
    elif comando == "VERDE_ON":
        verde.value(1)
        print("LED VERDE ENCENDIDO")

    elif comando == "VERDE_OFF":
        verde.value(0)
        print("LED VERDE APAGADO")

    # AMBOS LEDS
    elif comando == "TODOS_ON":
        rojo.value(1)
        verde.value(1)
        print("ROJO Y VERDE ENCENDIDOS")

    elif comando == "TODOS_OFF":
        rojo.value(0)
        verde.value(0)
        print("ROJO Y VERDE APAGADOS")

    else:
        print("COMANDO NO RECONOCIDO:", comando)
