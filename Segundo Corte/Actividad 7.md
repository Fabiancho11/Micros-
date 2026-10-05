<p><strong>Integrantes:</strong></p>
<ul>
    <li>Jeicob David Pinilla Ruiz</li>
    <li>Fabian Abril Casallas</li>
</ul>

<p align="center">
    <h1 align="center"><b>NAVEGACIÓN CON FEROMONAS POR RED</b></h1>
</p>

<p align="center">
    <b>ESP32 + Wi-Fi + UDP + PyBullet</b>
</p>

<p>
En este proyecto se utilizan tres carritos controlados mediante ESP32 para simular
el comportamiento de hormigas que buscan la salida de un laberinto.
Cada carrito utiliza un algoritmo basado en feromonas para seleccionar su
siguiente movimiento.
</p>

<p>
Mientras los carritos se desplazan por el laberinto, depositan feromonas en las
posiciones visitadas. Estas feromonas son intercambiadas mediante una red Wi-Fi
utilizando comunicación UDP.
</p>

<p>
Un computador central recibe las coordenadas de los tres ESP32, actualiza sus
posiciones y representa los carritos en tiempo real mediante PyBullet.
Además, el computador retransmite las feromonas recibidas hacia los demás
carritos para permitir el intercambio de información entre ellos.
</p>

<h2><b>Diagrama de bloques</b></h2>

<p align="center">
    <img src="../Imagenes/bloque_feromonas.png"
         alt="Diagrama de bloques del sistema de navegación con feromonas"
         width="800">
</p>

<hr>

<h2><b>Funcionamiento</b></h2>

<p>
El sistema está compuesto por tres ESP32 que representan los carritos
autónomos y un computador que funciona como servidor central.
</p>

<p>
Cada ESP32 conoce el mapa del laberinto y su posición inicial. En cada paso,
analiza las posiciones vecinas disponibles y calcula una probabilidad de
movimiento utilizando dos factores principales: la cantidad de feromona
presente en cada posición y la distancia hasta la meta.
</p>

<p>
Cuando un carrito se desplaza, deposita una cantidad de feromona en la nueva
posición y envía al computador sus coordenadas mediante UDP.
</p>

<p>
El computador recibe esta información y actualiza la representación del
carrito correspondiente en PyBullet. Posteriormente, la feromona depositada
se envía a los demás ESP32 para que puedan utilizarla durante su navegación.
</p>

<p align="center">
    <img src="../Imagenes/pybullet_feromonas.png"
         alt="Simulación del laberinto y los tres carritos en PyBullet"
         width="800">
</p>

<p>
En la simulación, cada carrito tiene un color diferente para facilitar su
identificación:
</p>

<ul>
    <li><strong>ESP32_1:</strong> Carro amarillo.</li>
    <li><strong>ESP32_2:</strong> Carro azul.</li>
    <li><strong>ESP32_3:</strong> Carro verde.</li>
</ul>

<p>
La meta se encuentra en la coordenada <strong>(7, 1)</strong> del laberinto.
Los tres carritos comienzan en diferentes posiciones y avanzan utilizando la
información de las feromonas compartidas.
</p>

<hr>

<h2><b>Video del funcionamiento</b></h2>

<p>
En el siguiente video se puede observar el funcionamiento del sistema,
incluyendo el movimiento de los tres carritos, la comunicación mediante
Wi-Fi y la visualización del gemelo digital en PyBullet.
</p>

<p align="center">
    <!-- Reemplazar el enlace por el video real -->
    <a href="https://youtu.be/TUV_ENLACE_AQUI" target="_blank">
        <b>Ver video del funcionamiento en YouTube</b>
    </a>
</p>

<hr>

<h2><b>1. Código del servidor PC - Python + PyBullet</b></h2>

<p>
Este programa se ejecuta en el computador y funciona como servidor central del
sistema. Utiliza comunicación UDP para recibir las posiciones de los ESP32 y
retransmitir la información de las feromonas.
</p>

<p>
También crea el gemelo digital del laberinto utilizando PyBullet y representa
cada ESP32 mediante un cuerpo de diferente color.
</p>

<pre>
<code>
import socket
import json
import threading
import time
import pybullet as p
import pybullet_data


# =========================================================
# CONFIGURACIÓN DEL SERVIDOR
# =========================================================

PORT = 5005


# =========================================================
# CONFIGURACIÓN DEL LABERINTO
# =========================================================

W, H = 13, 13

GRID = [
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# =========================================================
# META Y POSICIONES INICIALES
# =========================================================

GOAL = (7, 1)

STARTS = {
    "ESP32_1": (1, 11),
    "ESP32_2": (5, 11),
    "ESP32_3": (9, 11)
}


# =========================================================
# POSICIONES DE LOS ROBOTS
# =========================================================

robots = {
    "ESP32_1": {
        "x": STARTS["ESP32_1"][0],
        "y": STARTS["ESP32_1"][1]
    },

    "ESP32_2": {
        "x": STARTS["ESP32_2"][0],
        "y": STARTS["ESP32_2"][1]
    },

    "ESP32_3": {
        "x": STARTS["ESP32_3"][0],
        "y": STARTS["ESP32_3"][1]
    }
}


# =========================================================
# CLIENTES ESP32 Y PROTECCIÓN DE DATOS
# =========================================================

clientes_esp = set()

lock = threading.Lock()


# =========================================================
# SOCKET UDP
# =========================================================

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

sock.bind(
    ("0.0.0.0", PORT)
)

sock.settimeout(0.2)


# =========================================================
# SERVIDOR UDP
# =========================================================

def servidor():

    print(
        f"Servidor UDP en puerto {PORT}"
    )

    while True:

        try:

            datos, addr = sock.recvfrom(1024)

            clientes_esp.add(addr)

            msg = json.loads(
                datos.decode()
            )

            rid = msg.get("id")


            # -------------------------------------------------
            # Actualizar posición del robot
            # -------------------------------------------------

            if rid in robots:

                with lock:

                    robots[rid]["x"] = int(
                        msg.get(
                            "x",
                            robots[rid]["x"]
                        )
                    )

                    robots[rid]["y"] = int(
                        msg.get(
                            "y",
                            robots[rid]["y"]
                        )
                    )


                # -------------------------------------------------
                # Recibir feromona depositada
                # -------------------------------------------------

                ph_dep = float(
                    msg.get(
                        "ph_dep",
                        0.0
                    )
                )


                if ph_dep > 0:

                    paquete_update = json.dumps({

                        "cmd": "ph_update",

                        "x": robots[rid]["x"],

                        "y": robots[rid]["y"],

                        "v": ph_dep

                    }).encode()


                    # -------------------------------------------------
                    # Enviar feromona a los demás ESP32
                    # -------------------------------------------------

                    for cliente in clientes_esp:

                        if cliente != addr:

                            sock.sendto(
                                paquete_update,
                                cliente
                            )


        except socket.timeout:

            pass


        except Exception:

            pass


# =========================================================
# CREAR OBJETOS 3D
# =========================================================

def crear_caja(
    pos,
    half_extents,
    masa=0,
    color=(0.7, 0.7, 0.7, 1)
):

    col = p.createCollisionShape(
        p.GEOM_BOX,
        halfExtents=half_extents
    )


    vis = p.createVisualShape(
        p.GEOM_BOX,
        halfExtents=half_extents,
        rgbaColor=color
    )


    return p.createMultiBody(

        baseMass=masa,

        baseCollisionShapeIndex=col,

        baseVisualShapeIndex=vis,

        basePosition=pos

    )


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

def main():

    # -----------------------------------------------------
    # Iniciar servidor UDP
    # -----------------------------------------------------

    thread = threading.Thread(
        target=servidor,
        daemon=True
    )

    thread.start()


    # -----------------------------------------------------
    # Iniciar PyBullet
    # -----------------------------------------------------

    p.connect(p.GUI)

    p.setAdditionalSearchPath(
        pybullet_data.getDataPath()
    )

    p.setGravity(
        0,
        0,
        -9.81
    )


    p.resetDebugVisualizerCamera(

        cameraDistance=16,

        cameraYaw=0,

        cameraPitch=-80,

        cameraTargetPosition=[
            W / 2,
            H / 2,
            0
        ]

    )


    # -----------------------------------------------------
    # Crear suelo
    # -----------------------------------------------------

    plane_id = p.createCollisionShape(

        p.GEOM_BOX,

        halfExtents=[
            W / 2,
            H / 2,
            0.05
        ]

    )


    p.createMultiBody(

        0,

        plane_id,

        -1,

        [
            W / 2 - 0.5,
            H / 2 - 0.5,
            -0.05
        ]

    )


    # -----------------------------------------------------
    # Construir laberinto
    # -----------------------------------------------------

    for y in range(H):

        for x in range(W):

            if GRID[y][x] == 1:

                crear_caja(

                    [
                        x,
                        y,
                        0.5
                    ],

                    [
                        0.48,
                        0.48,
                        0.5
                    ],

                    0,

                    (
                        0.25,
                        0.25,
                        0.28,
                        1
                    )

                )


    # -----------------------------------------------------
    # Crear meta
    # -----------------------------------------------------

    crear_caja(

        [
            GOAL[0],
            GOAL[1],
            0.02
        ],

        [
            0.42,
            0.42,
            0.02
        ],

        0,

        (
            0.1,
            0.9,
            0.1,
            1
        )

    )


    # -----------------------------------------------------
    # Colores de los ESP32
    # -----------------------------------------------------

    COLOR_AMARILLO = (
        1.0,
        0.85,
        0.0,
        1.0
    )

    COLOR_AZUL = (
        0.1,
        0.4,
        0.9,
        1.0
    )

    COLOR_VERDE = (
        0.1,
        0.8,
        0.2,
        1.0
    )


    # -----------------------------------------------------
    # Crear carritos
    # -----------------------------------------------------

    cuerpos = {

        "ESP32_1": crear_caja(

            [
                STARTS["ESP32_1"][0],
                STARTS["ESP32_1"][1],
                0.35
            ],

            [
                0.3,
                0.22,
                0.2
            ],

            1.0,

            COLOR_AMARILLO

        ),


        "ESP32_2": crear_caja(

            [
                STARTS["ESP32_2"][0],
                STARTS["ESP32_2"][1],
                0.35
            ],

            [
                0.3,
                0.22,
                0.2
            ],

            1.0,

            COLOR_AZUL

        ),


        "ESP32_3": crear_caja(

            [
                STARTS["ESP32_3"][0],
                STARTS["ESP32_3"][1],
                0.35
            ],

            [
                0.3,
                0.22,
                0.2
            ],

            1.0,

            COLOR_VERDE

        )

    }


    print(
        "PyBullet iniciado con colores personalizados."
    )


    # -----------------------------------------------------
    # Bucle principal de simulación
    # -----------------------------------------------------

    while p.isConnected():

        with lock:

            datos = {
                rid: dict(v)
                for rid, v in robots.items()
            }


        for rid, info in datos.items():

            p.resetBasePositionAndOrientation(

                cuerpos[rid],

                [
                    info["x"],
                    info["y"],
                    0.35
                ],

                [
                    0,
                    0,
                    0,
                    1
                ]

            )


        p.stepSimulation()

        time.sleep(
            1 / 60
        )


    p.disconnect()


# =========================================================
# INICIO DEL PROGRAMA
# =========================================================

if __name__ == "__main__":

    main()
</code>
</pre>

<hr>

<h2><b>2. Código MicroPython - ESP32_1 - Carro Amarillo</b></h2>

<p>
Este programa corresponde al primer carrito. La ESP32 se conecta a la red
Wi-Fi, se comunica con el computador mediante UDP y utiliza el algoritmo de
selección basado en feromonas para decidir su siguiente posición.
</p>

<p>
El carro amarillo comienza en la coordenada <strong>(1, 11)</strong> y tiene
como objetivo llegar a la posición <strong>(7, 1)</strong>.
</p>

<pre>
<code>
import network
import socket
import time
import json
import random


# =========================================================
# CONFIGURACIÓN WI-FI
# =========================================================

SSID = "TVC_FAMILIAABRIL"

PASSWORD = "SeA1ft81oD"

PC_IP = "192.168.1.2"

PC_PORT = 5005


# =========================================================
# IDENTIFICACIÓN DEL ROBOT
# =========================================================

ROBOT_ID = "ESP32_1"


# =========================================================
# CONFIGURACIÓN DEL LABERINTO
# =========================================================

W, H = 13, 13

GRID = [
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# =========================================================
# META
# =========================================================

GOAL = (7, 1)


# =========================================================
# POSICIÓN INICIAL
# =========================================================

x, y = 1, 11

visitados = set([
    (x, y)
])


# =========================================================
# MAPA DE FEROMONAS
# =========================================================

pheromone = {}

for r in range(H):

    for c in range(W):

        if GRID[r][c] == 0:

            pheromone[
                (c, r)
            ] = 1.0


# =========================================================
# CONEXIÓN WI-FI
# =========================================================

wlan = network.WLAN(
    network.STA_IF
)

wlan.active(True)

wlan.connect(
    SSID,
    PASSWORD
)


while not wlan.isconnected():

    time.sleep(0.5)


# =========================================================
# SOCKET UDP
# =========================================================

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.setblocking(False)


# =========================================================
# FUNCIÓN PARA OBTENER VECINOS
# =========================================================

def vecinos(px, py):

    v = []

    for dx, dy in [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]:

        nx = px + dx
        ny = py + dy


        if (
            0 <= nx < W
            and 0 <= ny < H
            and GRID[ny][nx] == 0
        ):

            v.append(
                (nx, ny)
            )


    return v


# =========================================================
# FUNCIÓN HEURÍSTICA
# =========================================================

def heuristica(px, py):

    return 1.0 / (
        1
        + abs(px - GOAL[0])
        + abs(py - GOAL[1])
    )


# =========================================================
# SELECCIONAR SIGUIENTE POSICIÓN
# =========================================================

def elegir_siguiente():

    candidatos = [

        v
        for v in vecinos(x, y)
        if v not in visitados

    ]


    if not candidatos:

        candidatos = vecinos(x, y)

        if not candidatos:

            return (x, y)


    pesos = []


    for v in candidatos:

        tau = pheromone.get(
            v,
            1.0
        )

        eta = heuristica(
            v[0],
            v[1]
        )


        pesos.append(

            (tau ** 1.2)
            *
            (eta ** 3.0)

        )


    total = sum(pesos)


    if total <= 0:

        return random.choice(
            candidatos
        )


    r = random.random() * total

    acum = 0


    for i, w in enumerate(pesos):

        acum += w

        if r <= acum:

            return candidatos[i]


    return candidatos[-1]


# =========================================================
# TEMPORIZADOR DE MOVIMIENTO
# =========================================================

ultimo_paso = time.ticks_ms()


# =========================================================
# BUCLE PRINCIPAL
# =========================================================

while True:

    # -----------------------------------------------------
    # Recibir feromonas de otros ESP32
    # -----------------------------------------------------

    try:

        data, addr = sock.recvfrom(512)

        msg = json.loads(
            data.decode()
        )


        if msg.get("cmd") == "ph_update":

            px = msg["x"]

            py = msg["y"]

            pval = msg["v"]


            pheromone[
                (px, py)
            ] = (

                pheromone.get(
                    (px, py),
                    1.0
                )

                + pval

            )


    except:

        pass


    # -----------------------------------------------------
    # Realizar movimiento cada segundo
    # -----------------------------------------------------

    if time.ticks_diff(
        time.ticks_ms(),
        ultimo_paso
    ) > 1000:


        if (x, y) != GOAL:

            nx, ny = elegir_siguiente()


            visitados.add(
                (nx, ny)
            )


            x, y = nx, ny


            # -------------------------------------------------
            # Depositar feromona
            # -------------------------------------------------

            deposito = 0.5


            pheromone[
                (x, y)
            ] = (

                pheromone.get(
                    (x, y),
                    1.0
                )

                + deposito

            )


            # -------------------------------------------------
            # Enviar posición al PC
            # -------------------------------------------------

            paquete = {

                "id": ROBOT_ID,

                "x": x,

                "y": y,

                "ph_dep": deposito

            }


            sock.sendto(

                json.dumps(
                    paquete
                ).encode(),

                (
                    PC_IP,
                    PC_PORT
                )

            )


            print(
                f"{ROBOT_ID} "
                f"se movió a {x},{y}"
            )


        ultimo_paso = time.ticks_ms()


    time.sleep_ms(50)
</code>
</pre>

<hr>

<h2><b>3. Código MicroPython - ESP32_2 - Carro Azul</b></h2>

<p>
Este programa corresponde al segundo carrito. Su funcionamiento es equivalente
al del ESP32_1, pero utiliza el identificador <strong>ESP32_2</strong> y comienza
en una posición diferente del laberinto.
</p>

<p>
El carro azul comienza en la coordenada <strong>(5, 11)</strong>. Recibe las
feromonas enviadas por el computador y las utiliza para modificar las
probabilidades de selección de sus siguientes movimientos.
</p>

<pre>
<code>
import network
import socket
import time
import json
import random


# =========================================================
# CONFIGURACIÓN WI-FI
# =========================================================

SSID = "TVC_FAMILIAABRIL"

PASSWORD = "SeA1ft81oD"

PC_IP = "192.168.1.2"

PC_PORT = 5005


# =========================================================
# IDENTIFICACIÓN DEL ROBOT
# =========================================================

ROBOT_ID = "ESP32_2"


# =========================================================
# CONFIGURACIÓN DEL LABERINTO
# =========================================================

W, H = 13, 13

GRID = [
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# =========================================================
# META Y POSICIÓN INICIAL
# =========================================================

GOAL = (7, 1)

x, y = 5, 11

visitados = set([
    (x, y)
])


# =========================================================
# MAPA DE FEROMONAS
# =========================================================

pheromone = {}

for r in range(H):

    for c in range(W):

        if GRID[r][c] == 0:

            pheromone[
                (c, r)
            ] = 1.0


# =========================================================
# CONEXIÓN WI-FI
# =========================================================

wlan = network.WLAN(
    network.STA_IF
)

wlan.active(True)

wlan.connect(
    SSID,
    PASSWORD
)


while not wlan.isconnected():

    time.sleep(0.5)


# =========================================================
# SOCKET UDP
# =========================================================

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.setblocking(False)


# =========================================================
# OBTENER VECINOS
# =========================================================

def vecinos(px, py):

    v = []

    for dx, dy in [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]:

        nx = px + dx

        ny = py + dy


        if (
            0 <= nx < W
            and 0 <= ny < H
            and GRID[ny][nx] == 0
        ):

            v.append(
                (nx, ny)
            )


    return v


# =========================================================
# FUNCIÓN HEURÍSTICA
# =========================================================

def heuristica(px, py):

    return 1.0 / (
        1
        + abs(px - GOAL[0])
        + abs(py - GOAL[1])
    )


# =========================================================
# SELECCIÓN DEL SIGUIENTE MOVIMIENTO
# =========================================================

def elegir_siguiente():

    candidatos = [

        v
        for v in vecinos(x, y)
        if v not in visitados

    ]


    if not candidatos:

        candidatos = vecinos(x, y)

        if not candidatos:

            return (x, y)


    pesos = []


    for v in candidatos:

        tau = pheromone.get(
            v,
            1.0
        )

        eta = heuristica(
            v[0],
            v[1]
        )


        pesos.append(

            (tau ** 1.2)
            *
            (eta ** 3.0)

        )


    total = sum(pesos)


    if total <= 0:

        return random.choice(
            candidatos
        )


    r = random.random() * total

    acum = 0


    for i, w in enumerate(pesos):

        acum += w

        if r <= acum:

            return candidatos[i]


    return candidatos[-1]


# =========================================================
# TEMPORIZADOR
# =========================================================

ultimo_paso = time.ticks_ms()


# =========================================================
# BUCLE PRINCIPAL
# =========================================================

while True:

    # -----------------------------------------------------
    # Recibir feromonas
    # -----------------------------------------------------

    try:

        data, addr = sock.recvfrom(512)

        msg = json.loads(
            data.decode()
        )


        if msg.get("cmd") == "ph_update":

            px = msg["x"]

            py = msg["y"]

            pval = msg["v"]


            pheromone[
                (px, py)
            ] = (

                pheromone.get(
                    (px, py),
                    1.0
                )

                + pval

            )


    except:

        pass


    # -----------------------------------------------------
    # Movimiento
    # -----------------------------------------------------

    if time.ticks_diff(
        time.ticks_ms(),
        ultimo_paso
    ) > 1000:


        if (x, y) != GOAL:

            nx, ny = elegir_siguiente()


            visitados.add(
                (nx, ny)
            )


            x, y = nx, ny


            # -------------------------------------------------
            # Depositar feromona
            # -------------------------------------------------

            deposito = 0.5


            pheromone[
                (x, y)
            ] = (

                pheromone.get(
                    (x, y),
                    1.0
                )

                + deposito

            )


            # -------------------------------------------------
            # Enviar datos al PC
            # -------------------------------------------------

            paquete = {

                "id": ROBOT_ID,

                "x": x,

                "y": y,

                "ph_dep": deposito

            }


            sock.sendto(

                json.dumps(
                    paquete
                ).encode(),

                (
                    PC_IP,
                    PC_PORT
                )

            )


            print(
                f"{ROBOT_ID} "
                f"se movió a {x},{y}"
            )


        ultimo_paso = time.ticks_ms()


    time.sleep_ms(50)
</code>
</pre>

<hr>

<h2><b>4. Código MicroPython - ESP32_3 - Carro Verde</b></h2>

<p>
Este programa corresponde al tercer carrito del sistema. Utiliza la misma
lógica de navegación y comunicación que los otros dos ESP32, pero tiene el
identificador <strong>ESP32_3</strong> y una posición inicial diferente.
</p>

<p>
El carro verde comienza en la coordenada <strong>(9, 11)</strong> y comparte
la información de feromonas con los otros carritos mediante el computador
central.
</p>

<pre>
<code>
import network
import socket
import time
import json
import random


# =========================================================
# CONFIGURACIÓN WI-FI
# =========================================================

SSID = "TVC_FAMILIAABRIL"

PASSWORD = "SeA1ft81oD"

PC_IP = "192.168.1.2"

PC_PORT = 5005


# =========================================================
# IDENTIFICACIÓN DEL ROBOT
# =========================================================

ROBOT_ID = "ESP32_3"


# =========================================================
# CONFIGURACIÓN DEL LABERINTO
# =========================================================

W, H = 13, 13

GRID = [
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# =========================================================
# META Y POSICIÓN INICIAL
# =========================================================

GOAL = (7, 1)

x, y = 9, 11

visitados = set([
    (x, y)
])


# =========================================================
# MAPA DE FEROMONAS
# =========================================================

pheromone = {}

for r in range(H):

    for c in range(W):

        if GRID[r][c] == 0:

            pheromone[
                (c, r)
            ] = 1.0


# =========================================================
# CONEXIÓN WI-FI
# =========================================================

wlan = network.WLAN(
    network.STA_IF
)

wlan.active(True)

wlan.connect(
    SSID,
    PASSWORD
)


while not wlan.isconnected():

    time.sleep(0.5)


# =========================================================
# SOCKET UDP
# =========================================================

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.setblocking(False)


# =========================================================
# OBTENER VECINOS
# =========================================================

def vecinos(px, py):

    v = []

    for dx, dy in [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]:

        nx = px + dx

        ny = py + dy


        if (
            0 <= nx < W
            and 0 <= ny < H
            and GRID[ny][nx] == 0
        ):

            v.append(
                (nx, ny)
            )


    return v


# =========================================================
# FUNCIÓN HEURÍSTICA
# =========================================================

def heuristica(px, py):

    return 1.0 / (
        1
        + abs(px - GOAL[0])
        + abs(py - GOAL[1])
    )


# =========================================================
# SELECCIONAR SIGUIENTE POSICIÓN
# =========================================================

def elegir_siguiente():

    candidatos = [

        v
        for v in vecinos(x, y)
        if v not in visitados

    ]


    if not candidatos:

        candidatos = vecinos(x, y)

        if not candidatos:

            return (x, y)


    pesos = []


    for v in candidatos:

        tau = pheromone.get(
            v,
            1.0
        )

        eta = heuristica(
            v[0],
            v[1]
        )


        pesos.append(

            (tau ** 1.2)
            *
            (eta ** 3.0)

        )


    total = sum(pesos)


    if total <= 0:

        return random.choice(
            candidatos
        )


    r = random.random() * total

    acum = 0


    for i, w in enumerate(pesos):

        acum += w

        if r <= acum:

            return candidatos[i]


    return candidatos[-1]


# =========================================================
# TEMPORIZADOR
# =========================================================

ultimo_paso = time.ticks_ms()


# =========================================================
# BUCLE PRINCIPAL
# =========================================================

while True:

    # -----------------------------------------------------
    # Recibir feromonas
    # -----------------------------------------------------

    try:

        data, addr = sock.recvfrom(512)

        msg = json.loads(
            data.decode()
        )


        if msg.get("cmd") == "ph_update":

            px = msg["x"]

            py = msg["y"]

            pval = msg["v"]


            pheromone[
                (px, py)
            ] = (

                pheromone.get(
                    (px, py),
                    1.0
                )

                + pval

            )


    except:

        pass


    # -----------------------------------------------------
    # Movimiento
    # -----------------------------------------------------

    if time.ticks_diff(
        time.ticks_ms(),
        ultimo_paso
    ) > 1000:


        if (x, y) != GOAL:

            nx, ny = elegir_siguiente()


            visitados.add(
                (nx, ny)
            )


            x, y = nx, ny


            # -------------------------------------------------
            # Depositar feromona
            # -------------------------------------------------

            deposito = 0.5


            pheromone[
                (x, y)
            ] = (

                pheromone.get(
                    (x, y),
                    1.0
                )

                + deposito

            )


            # -------------------------------------------------
            # Enviar datos al PC
            # -------------------------------------------------

            paquete = {

                "id": ROBOT_ID,

                "x": x,

                "y": y,

                "ph_dep": deposito

            }


            sock.sendto(

                json.dumps(
                    paquete
                ).encode(),

                (
                    PC_IP,
                    PC_PORT
                )

            )


            print(
                f"{ROBOT_ID} "
                f"se movió a {x},{y}"
            )


        ultimo_paso = time.ticks_ms()


    time.sleep_ms(50)
</code>
</pre>

<hr>

<h2><b>5. Algoritmo de navegación por feromonas</b></h2>

<p>
Para seleccionar el siguiente movimiento se consideran las posiciones vecinas
que están libres dentro del laberinto. A cada posición se le asigna un peso
dependiendo de la cantidad de feromona y de su distancia hasta la meta.
</p>

<p>
La ecuación utilizada para calcular el peso de cada posición es:
</p>

<p align="center">
    <b>
        P = &tau;<sup>1.2</sup> &times; &eta;<sup>3.0</sup>
    </b>
</p>

<p>
donde <strong>&tau;</strong> representa la cantidad de feromona almacenada en
la posición y <strong>&eta;</strong> corresponde a la función heurística basada
en la distancia Manhattan hasta la meta.
</p>

<p>
La heurística utilizada es:
</p>

<p align="center">
    <b>
        &eta; = 1 / (1 + |x - x<sub>meta</sub>| + |y - y<sub>meta</sub>|)
    </b>
</p>

<p>
Después de calcular los pesos, se realiza una selección probabilística del
siguiente movimiento. De esta forma, los carritos pueden utilizar la
información dejada previamente por otros carritos y continuar explorando el
laberinto.
</p>

<hr>

<h2><b>6. Comunicación entre ESP32 y computador</b></h2>

<p>
La comunicación se realiza mediante paquetes UDP enviados a través de la red
Wi-Fi. Cada paquete enviado desde una ESP32 contiene el identificador del
carrito, sus coordenadas actuales y la cantidad de feromona depositada.
</p>

<pre>
<code>
paquete = {
    "id": ROBOT_ID,
    "x": x,
    "y": y,
    "ph_dep": deposito
}
</code>
</pre>

<p>
El computador recibe estos datos en el puerto <strong>5005</strong>. Después
de recibir una feromona, genera un mensaje con el comando
<strong>ph_update</strong> y lo envía a los demás ESP32 conectados.
</p>

<pre>
<code>
{
    "cmd": "ph_update",
    "x": x,
    "y": y,
    "v": ph_dep
}
</code>
</pre>

<hr>

<h2><b>7. Gemelo digital en PyBullet</b></h2>

<p>
El computador funciona como un gemelo digital del sistema físico. Las
coordenadas recibidas desde los ESP32 se utilizan para actualizar en tiempo
real la posición de los tres carritos dentro del entorno virtual.
</p>

<p>
El laberinto está construido a partir de una matriz de 13 &times; 13,
donde el valor <strong>1</strong> representa una pared y el valor
<strong>0</strong> representa una posición libre para el movimiento.
</p>

<p>
Los tres carritos son representados mediante cuerpos 3D con diferentes
colores, permitiendo observar simultáneamente el movimiento de los robots
físicos y su representación virtual.
</p>

<hr>

<h2><b>8. Distribución de los carritos</b></h2>

<table border="1" cellpadding="8" cellspacing="0" align="center">
    <tr>
        <th>Robot</th>
        <th>Color</th>
        <th>Posición inicial</th>
        <th>Meta</th>
    </tr>

    <tr>
        <td>ESP32_1</td>
        <td>Amarillo</td>
        <td>(1, 11)</td>
        <td>(7, 1)</td>
    </tr>

    <tr>
        <td>ESP32_2</td>
        <td>Azul</td>
        <td>(5, 11)</td>
        <td>(7, 1)</td>
    </tr>

    <tr>
        <td>ESP32_3</td>
        <td>Verde</td>
        <td>(9, 11)</td>
        <td>(7, 1)</td>
    </tr>
</table>

<hr>

<h2><b>9. Resumen del sistema</b></h2>

<p>
El proyecto integra sistemas embebidos, comunicación inalámbrica, algoritmos
de navegación y simulación 3D. Los tres ESP32 funcionan como agentes
independientes que exploran el mismo laberinto y comparten información sobre
las posiciones donde se han depositado feromonas.
</p>

<p>
El computador recibe esta información mediante UDP y actúa como servidor
central. Además de retransmitir las feromonas, mantiene un gemelo digital
realizado en PyBullet que permite visualizar el movimiento de los tres
carritos en tiempo real.
</p>

<p>
De esta manera, el sistema combina el comportamiento cooperativo de varios
robots con comunicación por red y una representación virtual del entorno
físico.
</p>
