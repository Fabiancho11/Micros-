from ultralytics import YOLO
import cv2
import serial
import time

# ==========================================
# CONFIGURACIÓN SERIAL
# ==========================================

PUERTO = "COM3"
BAUDRATE = 115200

esp32 = serial.Serial(PUERTO, BAUDRATE, timeout=1)

time.sleep(2)

print("ESP32 conectado en", PUERTO)

# ==========================================
# CARGAR YOLO
# ==========================================

model = YOLO("yolo11n.pt")

# ==========================================
# CÁMARA
# ==========================================

cap = cv2.VideoCapture(0)

# ==========================================
# VARIABLES
# ==========================================

ultima_deteccion = ""

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("No se pudo abrir la cámara")
        break

    # --------------------------------------
    # YOLO
    # --------------------------------------

    results = model(
        frame,
        conf=0.25,
        verbose=False
    )

    deteccion_actual = ""

    # --------------------------------------
    # REVISAR OBJETOS
    # --------------------------------------

    for result in results:

        for box in result.boxes:

            clase = int(box.cls[0])
            confianza = float(box.conf[0])

            nombre = model.names[clase]

            # Mostrar en consola todo lo detectado
            print(
                "Objeto:",
                nombre,
                "Confianza:",
                round(confianza, 2)
            )

            # ==================================
            # CARRO
            # ==================================

            if nombre == "car":

                deteccion_actual = "CARRO"

            # ==================================
            # MOTO
            # ==================================

            elif nombre == "motorcycle":

                deteccion_actual = "MOTO"

    # --------------------------------------
    # ENVIAR AL ESP32
    # --------------------------------------

    if deteccion_actual != ultima_deteccion:

        if deteccion_actual == "CARRO":

            esp32.write(b"CARRO\n")
            print(">>> CARRO DE JUGUETE DETECTADO")

        elif deteccion_actual == "MOTO":

            esp32.write(b"MOTO\n")
            print(">>> MOTO DE JUGUETE DETECTADA")

        else:

            esp32.write(b"NINGUNO\n")
            print(">>> NINGUN OBJETO")

        ultima_deteccion = deteccion_actual

    # --------------------------------------
    # MOSTRAR CÁMARA
    # --------------------------------------

    imagen = results[0].plot()

    cv2.imshow(
        "YOLO - Juguetes",
        imagen
    )

    # --------------------------------------
    # SALIR
    # --------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# CERRAR
# ==========================================

cap.release()
cv2.destroyAllWindows()
esp32.close()