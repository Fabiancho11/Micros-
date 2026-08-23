# ESP-WROOM-32: Arquitectura, Características y Programación

## Introducción

La **ESP-WROOM-32**, comúnmente conocida como **ESP32**, es un módulo basado en un microcontrolador de bajo costo desarrollado por Espressif Systems. Su principal característica es que integra en un mismo sistema capacidades de procesamiento, memoria y comunicación inalámbrica mediante **Wi-Fi y Bluetooth**.

Gracias a estas características, la ESP32 se utiliza ampliamente en proyectos de **Internet de las Cosas (IoT)**, automatización, robótica, domótica, monitoreo de sensores y sistemas de adquisición de datos.

Una ventaja importante de esta familia de dispositivos es que permite conectar diferentes sensores y actuadores directamente a sus pines GPIO. Por ejemplo, es posible leer sensores analógicos, controlar motores mediante señales PWM, comunicarse con otros dispositivos usando protocolos como I2C, SPI o UART y enviar información a través de una red Wi-Fi.

![Placa ESP32](./Imagenes/ESP32.jpg)

*Figura 1. Placa de desarrollo basada en el módulo ESP-WROOM-32.*

---

# 1. ¿Qué es la ESP-WROOM-32?

La **ESP-WROOM-32** es un módulo que incorpora el chip ESP32 y los elementos necesarios para establecer comunicaciones inalámbricas. Este módulo puede encontrarse integrado en diferentes placas de desarrollo, siendo una de las más conocidas la **ESP32 DevKit V1**.

Es importante diferenciar entre el chip, el módulo y la placa de desarrollo:

* **ESP32:** es el microcontrolador o sistema en chip principal.
* **ESP-WROOM-32:** es el módulo que contiene el chip ESP32, la antena y otros componentes necesarios para su funcionamiento.
* **ESP32 DevKit:** es la placa de desarrollo que facilita la programación y conexión del módulo con sensores y otros dispositivos.

La placa de desarrollo permite programar fácilmente el microcontrolador desde un computador mediante un cable USB. También proporciona pines accesibles para conectar componentes externos.

---

# 2. Estructura de la ESP32

Una placa de desarrollo basada en ESP-WROOM-32 está formada por diferentes elementos. Cada uno cumple una función específica dentro del funcionamiento general del sistema.

## 2.1 Módulo ESP-WROOM-32

El módulo ESP-WROOM-32 contiene el microcontrolador principal y la antena utilizada para las comunicaciones inalámbricas. Generalmente se encuentra cubierto por una carcasa metálica que ayuda a reducir las interferencias electromagnéticas.

Este módulo es el encargado de ejecutar el programa y controlar los periféricos conectados.

![Módulo ESP-WROOM-32](./Imagenes/ESP-WROOM-32.jpg)

*Figura 2. Módulo ESP-WROOM-32.*

---

## 2.2 Antena Wi-Fi y Bluetooth

La mayoría de los módulos ESP-WROOM-32 incluyen una antena integrada en la propia placa.

Esta antena permite establecer comunicaciones mediante:

* Wi-Fi.
* Bluetooth clásico.
* Bluetooth Low Energy o BLE.

La integración de estas tecnologías en un mismo dispositivo es una de las razones por las que la ESP32 es ampliamente utilizada en aplicaciones IoT.

---

## 2.3 Conversor USB a UART

La computadora se comunica normalmente mediante USB, mientras que el microcontrolador utiliza comunicación serial UART.

Por esta razón, las placas de desarrollo incorporan un conversor USB a UART. Dependiendo del fabricante, pueden utilizarse circuitos integrados como:

* CP2102.
* CH340.
* FTDI.

Este componente permite cargar programas desde el computador hacia la memoria Flash de la ESP32.

---

## 2.4 Puerto USB

El puerto USB cumple principalmente dos funciones:

1. Alimentar la placa.
2. Permitir la comunicación entre la computadora y la ESP32.

La mayoría de las placas tradicionales ESP32 DevKit utilizan un conector Micro-USB, aunque versiones más recientes pueden utilizar USB-C.

---

## 2.5 Regulador de voltaje

Aunque la alimentación procedente del USB normalmente es de aproximadamente 5 V, el microcontrolador ESP32 trabaja internamente con niveles de 3.3 V.

Por esta razón, la placa incorpora un regulador de voltaje que reduce y estabiliza la tensión.

> **Importante:** Los pines GPIO de la ESP32 trabajan normalmente con niveles lógicos de 3.3 V. No se recomienda aplicar directamente 5 V a un GPIO.

---

## 2.6 Botón EN

El botón **EN**, también identificado en algunas placas como **Enable**, permite reiniciar el microcontrolador.

Su funcionamiento es equivalente a un botón de Reset. Al presionarlo, el programa vuelve a iniciar desde el comienzo.

---

## 2.7 Botón BOOT

El botón **BOOT** se utiliza principalmente durante el proceso de programación.

En determinadas placas, puede ser necesario mantener presionado este botón mientras se inicia la carga del programa para colocar la ESP32 en modo de programación.

---

## 2.8 Pines GPIO

Los pines GPIO, cuyo nombre significa **General Purpose Input/Output**, permiten conectar la ESP32 con dispositivos externos.

Estos pines pueden configurarse como:

* Entradas digitales.
* Salidas digitales.
* Entradas analógicas.
* Salidas PWM.
* Comunicación I2C.
* Comunicación SPI.
* Comunicación UART.
* Funciones táctiles capacitivas.

La posibilidad de asignar diferentes funciones a los pines proporciona una gran flexibilidad durante el diseño de proyectos electrónicos.

---

# 3. Arquitectura interna de la ESP32

La ESP32 se considera un **Sistema en un Chip o SoC (System on Chip)**. Esto significa que en un solo circuito integrado se encuentran varios elementos necesarios para el funcionamiento del sistema.

Su arquitectura incluye:

* Unidad de procesamiento.
* Memoria.
* Comunicación Wi-Fi.
* Comunicación Bluetooth.
* Convertidores ADC.
* Controladores PWM.
* Interfaces de comunicación.
* Temporizadores.
* Periféricos internos.

![Arquitectura de la ESP32](./Imagenes/Arquitectura_ESP32.jpg)

*Figura 3. Representación general de la arquitectura interna de la ESP32.*

---

# 4. Unidad Central de Procesamiento

La versión clásica del ESP32 utiliza procesadores basados en la arquitectura **Xtensa LX6 de 32 bits**.

Muchas versiones incorporan dos núcleos de procesamiento, lo que permite distribuir diferentes tareas.

Por ejemplo, un núcleo puede encargarse de tareas relacionadas con la comunicación inalámbrica, mientras el otro ejecuta la lógica principal del programa.

La frecuencia de funcionamiento puede alcanzar hasta:

**240 MHz**

Esta velocidad es considerablemente mayor que la de microcontroladores tradicionales como el Arduino Uno, que trabaja normalmente a 16 MHz.

La capacidad de procesamiento de la ESP32 permite desarrollar aplicaciones como:

* Procesamiento de señales.
* Sistemas de monitoreo.
* Control de motores.
* Interfaces gráficas.
* Comunicación con servidores.
* Automatización.
* Aplicaciones IoT.

---

# 5. Memoria de la ESP32

La ESP32 utiliza diferentes tipos de memoria.

| Tipo de memoria | Función                                                             |
| --------------- | ------------------------------------------------------------------- |
| ROM             | Contiene funciones fundamentales del sistema y procesos de arranque |
| SRAM            | Almacena variables y datos durante la ejecución                     |
| RTC Memory      | Permite conservar determinados datos en modos de bajo consumo       |
| Flash           | Almacena permanentemente el programa y otros archivos               |

## 5.1 Memoria ROM

La memoria ROM contiene información fundamental para el funcionamiento del dispositivo.

Entre sus funciones se encuentran procesos relacionados con el arranque del sistema y rutinas internas.

---

## 5.2 Memoria SRAM

La SRAM es utilizada como memoria de trabajo.

Aquí se almacenan elementos como:

* Variables.
* Arreglos.
* Datos temporales.
* Información utilizada durante la ejecución del programa.

---

## 5.3 Memoria Flash

La memoria Flash almacena el programa de manera permanente.

Cuando se carga un programa utilizando Arduino IDE, PlatformIO o MicroPython, el código queda almacenado en esta memoria.

Muchas placas ESP32 incluyen alrededor de 4 MB de memoria Flash, aunque existen módulos con diferentes capacidades.

---

# 6. Conectividad inalámbrica

Una de las principales características de la ESP32 es la integración de conectividad inalámbrica.

## 6.1 Wi-Fi

La ESP32 puede conectarse a redes inalámbricas mediante Wi-Fi.

Puede funcionar principalmente en dos modos:

### Modo Station

En este modo, la ESP32 se conecta a una red Wi-Fi existente, por ejemplo, a un router.

Esto permite enviar datos hacia:

* Servidores.
* Aplicaciones.
* Plataformas IoT.
* Computadoras.
* Servicios en la nube.

### Modo Access Point

En este modo, la ESP32 crea su propia red Wi-Fi.

Otros dispositivos, como teléfonos o computadores, pueden conectarse directamente a ella.

Esta función es útil cuando se desea controlar un dispositivo sin necesidad de utilizar un router.

---

## 6.2 Bluetooth

La ESP32 clásica incorpora soporte para:

* Bluetooth clásico.
* Bluetooth Low Energy (BLE).

Bluetooth clásico puede utilizarse para aplicaciones que requieren una comunicación convencional con teléfonos o computadores.

BLE está diseñado para aplicaciones que requieren un menor consumo de energía, por lo que resulta adecuado para sensores que funcionan con baterías.

---

# 7. Pines de la ESP32

Los pines GPIO son fundamentales para conectar dispositivos externos.

En una placa ESP32 DevKit es común encontrar pines como:

* GPIO 2.
* GPIO 4.
* GPIO 5.
* GPIO 12.
* GPIO 13.
* GPIO 14.
* GPIO 15.
* GPIO 16.
* GPIO 17.
* GPIO 18.
* GPIO 19.
* GPIO 21.
* GPIO 22.
* GPIO 23.
* GPIO 25.
* GPIO 26.
* GPIO 27.
* GPIO 32.
* GPIO 33.
* GPIO 34.
* GPIO 35.

![Pinout de la ESP32](./Imagenes/Pinout_ESP32.png)

*Figura 4. Distribución general de pines de una placa ESP32 DevKit.*

> **Nota:** La distribución física y la cantidad de pines pueden variar dependiendo del fabricante y de la versión de la placa.

---

# 8. Pines de alimentación

La placa normalmente dispone de los siguientes pines de alimentación:

| Pin      | Función                                                |
| -------- | ------------------------------------------------------ |
| VIN o 5V | Entrada o alimentación de 5 V, dependiendo de la placa |
| 3V3      | Alimentación de 3.3 V                                  |
| GND      | Tierra o referencia del circuito                       |

Todos los dispositivos conectados deben compartir una referencia común de tierra cuando sea necesario.

---

# 9. Entradas y salidas digitales

Los GPIO pueden utilizarse para leer o escribir señales digitales.

Una entrada digital puede utilizarse para conectar:

* Pulsadores.
* Interruptores.
* Sensores digitales.
* Detectores de presencia.

Una salida digital puede controlar:

* LEDs.
* Relés.
* Transistores.
* Módulos electrónicos.

En una salida digital existen dos estados principales:

* **LOW o nivel bajo.**
* **HIGH o nivel alto.**

Un ejemplo sencillo consiste en encender y apagar un LED.

```cpp
#define LED 2

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(1000);

  digitalWrite(LED, LOW);
  delay(1000);
}
```

---

# 10. ADC: Convertidor Analógico a Digital

El ADC permite convertir una señal de voltaje analógica en un valor digital que puede ser procesado por el microcontrolador.

Esta función es necesaria para trabajar con sensores que entregan una señal analógica.

Algunos ejemplos son:

* Potenciómetros.
* LDR.
* Sensores de presión.
* Sensores de fuerza.
* Sensores de voltaje.

La ESP32 clásica dispone de convertidores ADC de hasta 12 bits de resolución.

Esto permite representar una lectura utilizando valores entre:

**0 y 4095**

De forma general:

```text
0 V        → 0
Voltaje máximo de referencia → 4095
```

Un ejemplo de lectura analógica en Arduino es:

```cpp
#define SENSOR 34

void setup() {
  Serial.begin(115200);
}

void loop() {
  int valor = analogRead(SENSOR);

  Serial.println(valor);

  delay(500);
}
```

Los pines GPIO 34 y GPIO 35 son utilizados frecuentemente como entradas analógicas.

> **Importante:** Algunos GPIO tienen limitaciones específicas. Por ejemplo, GPIO 34, 35, 36 y 39 son únicamente de entrada.

---

# 11. PWM: Modulación por Ancho de Pulso

PWM significa **Pulse Width Modulation** o Modulación por Ancho de Pulso.

La señal PWM permite controlar la potencia promedio entregada a un dispositivo.

Entre sus aplicaciones se encuentran:

* Control del brillo de LEDs.
* Control de velocidad de motores.
* Control de servomotores.
* Generación de señales.

La ESP32 dispone de periféricos dedicados que permiten generar señales PWM con diferentes frecuencias y resoluciones.

En Arduino IDE puede utilizarse el sistema LEDC.

Un ejemplo para controlar el brillo de un LED es:

```cpp
#define LED 2

void setup() {
  ledcAttach(LED, 5000, 8);
}

void loop() {

  for (int brillo = 0; brillo <= 255; brillo++) {
    ledcWrite(LED, brillo);
    delay(10);
  }

  for (int brillo = 255; brillo >= 0; brillo--) {
    ledcWrite(LED, brillo);
    delay(10);
  }
}
```

En este caso, el LED aumenta y disminuye progresivamente su brillo.

---

# 12. DAC: Convertidor Digital a Analógico

El DAC realiza el proceso contrario al ADC.

Mientras que el ADC convierte un voltaje analógico en un número digital, el DAC convierte un valor digital en una señal de voltaje analógica.

En la ESP32 clásica existen dos canales DAC principales:

| Canal DAC | GPIO    |
| --------- | ------- |
| DAC1      | GPIO 25 |
| DAC2      | GPIO 26 |

Los DAC tienen una resolución de 8 bits.

Por lo tanto, pueden utilizar valores entre:

**0 y 255**

Un ejemplo sencillo es:

```cpp
#define DAC_PIN 25

void setup() {
}

void loop() {

  dacWrite(DAC_PIN, 128);

}
```

Este valor genera aproximadamente un nivel intermedio de la salida disponible.

El DAC puede utilizarse para:

* Generar señales.
* Producir audio básico.
* Generar voltajes de referencia.
* Realizar experimentos de electrónica analógica.

---

# 13. Interfaces de comunicación

La ESP32 cuenta con diferentes protocolos para comunicarse con otros dispositivos.

## 13.1 UART

UART es una comunicación serial.

Se utiliza para conectar dispositivos como:

* GPS.
* Módulos Bluetooth externos.
* Computadoras.
* Otros microcontroladores.

La comunicación se realiza normalmente utilizando dos líneas principales:

* TX: transmisión.
* RX: recepción.

---

## 13.2 I2C

I2C permite conectar múltiples dispositivos utilizando únicamente dos líneas principales:

* SDA: datos.
* SCL: reloj.

En muchas placas ESP32 se utilizan frecuentemente:

```text
SDA = GPIO 21
SCL = GPIO 22
```

Sin embargo, la ESP32 permite configurar otros pines para esta función.

I2C se utiliza frecuentemente para conectar:

* Pantallas LCD.
* MPU6050.
* Sensores de temperatura.
* Relojes RTC.

---

## 13.3 SPI

SPI es un protocolo de comunicación de alta velocidad.

Puede utilizarse con:

* Pantallas.
* Tarjetas SD.
* Módulos RFID.
* Convertidores.
* Sensores.

Las líneas principales son:

* MOSI.
* MISO.
* SCK.
* CS.

---

# 14. Programación de la ESP32 en C/C++

La ESP32 puede programarse utilizando Arduino IDE y el framework de Arduino.

En este entorno se utiliza principalmente C/C++.

## Ventajas de C/C++

### Mayor rendimiento

El código compilado puede ejecutarse de forma más eficiente.

Esto es importante en aplicaciones que requieren:

* Mayor velocidad.
* Procesamiento en tiempo real.
* Control preciso de periféricos.

### Mayor control del hardware

C/C++ permite trabajar directamente con registros, memoria y periféricos del microcontrolador.

### Amplia disponibilidad de librerías

Existen numerosas librerías para sensores y dispositivos.

### Adecuado para proyectos complejos

Es una buena opción para sistemas que requieren:

* Wi-Fi.
* Bluetooth.
* Control de motores.
* Sensores.
* Interfaces gráficas.
* Procesamiento de datos.

## Desventajas de C/C++

### Mayor dificultad para principiantes

Es necesario comprender conceptos como:

* Tipos de datos.
* Funciones.
* Punteros.
* Memoria.
* Estructuras.

### Compilación

El programa debe ser compilado antes de ejecutarse.

Esto puede hacer que el ciclo de desarrollo sea más lento en comparación con un lenguaje interpretado.

### Errores de programación

Los errores relacionados con la memoria o el manejo incorrecto de datos pueden ser más difíciles de detectar.

---

# 15. Programación de la ESP32 en MicroPython

MicroPython es una implementación de Python diseñada para funcionar en microcontroladores.

Permite escribir programas utilizando una sintaxis similar a Python.

Un ejemplo para encender y apagar un LED es:

```python
from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)

while True:
    led.on()
    sleep(1)

    led.off()
    sleep(1)
```

## Ventajas de MicroPython

### Sintaxis sencilla

Python tiene una sintaxis fácil de leer.

Esto facilita el aprendizaje para personas que están comenzando a programar.

### Desarrollo rápido

Es posible realizar pruebas y modificar programas de manera rápida.

### REPL interactivo

MicroPython permite utilizar una consola interactiva llamada REPL.

Desde esta consola se pueden ejecutar instrucciones directamente en el microcontrolador.

Por ejemplo:

```python
>>> from machine import Pin
>>> led = Pin(2, Pin.OUT)
>>> led.on()
```

Esto permite probar periféricos sin necesidad de compilar un programa completo.

### Código fácil de entender

La sintaxis suele ser más corta y clara.

---

## Desventajas de MicroPython

### Menor rendimiento

MicroPython normalmente es más lento que un programa compilado en C/C++.

### Mayor uso de memoria

El intérprete de MicroPython requiere recursos adicionales.

### Menor disponibilidad de algunas librerías

Aunque existen muchas librerías, algunas funciones específicas pueden estar mejor soportadas en C/C++.

### Limitaciones en proyectos exigentes

Para aplicaciones que requieren tiempos muy precisos o un alto rendimiento, C/C++ puede ser una mejor alternativa.

---

# 16. Comparación entre C/C++ y MicroPython

| Característica           | C/C++          | MicroPython                        |
| ------------------------ | -------------- | ---------------------------------- |
| Velocidad de ejecución   | Alta           | Media                              |
| Facilidad de aprendizaje | Media          | Alta                               |
| Uso de memoria           | Menor          | Mayor                              |
| Compilación              | Necesaria      | No en el mismo sentido tradicional |
| Control del hardware     | Muy alto       | Alto                               |
| Desarrollo rápido        | Medio          | Alto                               |
| REPL interactivo         | No normalmente | Sí                                 |
| Aplicaciones exigentes   | Muy adecuado   | Puede tener limitaciones           |

---

# 17. Ventajas generales de la ESP32

La ESP32 presenta diferentes ventajas frente a otros microcontroladores.

* Bajo costo.
* Buen rendimiento.
* Procesadores de hasta 240 MHz en modelos clásicos.
* Conectividad Wi-Fi integrada.
* Bluetooth y BLE integrados en los modelos compatibles.
* Gran cantidad de GPIO.
* Entradas analógicas mediante ADC.
* Generación de PWM.
* Amplias opciones de comunicación.
* Compatibilidad con Arduino IDE.
* Compatibilidad con MicroPython.
* Gran cantidad de documentación y proyectos disponibles.
* Bajo consumo de energía en modos de ahorro.
* Posibilidad de utilizar modos de suspensión.

---

# 18. Desventajas generales de la ESP32

A pesar de sus ventajas, también existen algunas limitaciones.

* No todos los GPIO pueden utilizarse de la misma forma.
* Algunos pines tienen funciones especiales durante el arranque.
* Los niveles lógicos son de 3.3 V.
* La lectura ADC puede requerir calibración dependiendo de la aplicación.
* Algunas funciones cambian entre las diferentes versiones de la familia ESP32.
* El uso simultáneo de diferentes periféricos puede requerir una configuración cuidadosa.
* Algunas aplicaciones pueden consumir bastante corriente cuando se utiliza Wi-Fi.

---

# 19. Aplicaciones de la ESP32

Debido a su versatilidad, la ESP32 puede utilizarse en numerosos proyectos.

## Internet de las Cosas

La ESP32 puede leer sensores y enviar información a internet.

Ejemplos:

* Estaciones meteorológicas.
* Monitoreo de temperatura.
* Monitoreo de consumo eléctrico.
* Sistemas de seguridad.

## Domótica

Puede utilizarse para controlar dispositivos dentro de una vivienda.

Ejemplos:

* Luces inteligentes.
* Persianas automáticas.
* Control de temperatura.
* Sistemas de acceso.

## Robótica

La ESP32 permite controlar motores y recibir información de sensores.

Puede utilizarse en:

* Robots móviles.
* Brazos robóticos.
* Vehículos autónomos.
* Sistemas de navegación.

## Sistemas de monitoreo

Puede adquirir datos provenientes de diferentes sensores.

Por ejemplo:

```text
Sensor → ESP32 → Wi-Fi → Computadora o servidor
```

---

# 20. Ejemplo de conexión de un LED

Una conexión básica consiste en conectar un LED a un GPIO mediante una resistencia.

```text
GPIO 2 ---- Resistencia ---- LED ---- GND
```

El programa puede controlar el estado del LED.

```cpp
#define LED 2

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(1000);

  digitalWrite(LED, LOW);
  delay(1000);
}
```

Este programa genera un parpadeo con un periodo aproximado de un segundo encendido y un segundo apagado.

---

# 21. Conclusiones

La ESP-WROOM-32 representa una plataforma muy completa para el desarrollo de proyectos electrónicos. Su integración de procesamiento, Wi-Fi, Bluetooth y múltiples periféricos permite desarrollar sistemas conectados sin necesidad de utilizar módulos adicionales para las comunicaciones inalámbricas.

La gran cantidad de GPIO y la posibilidad de utilizar ADC, PWM, DAC, I2C, SPI y UART hacen que la placa sea adecuada para conectar diferentes tipos de sensores y actuadores.

La elección entre C/C++ y MicroPython depende principalmente de las necesidades del proyecto. MicroPython resulta especialmente útil para el aprendizaje y el desarrollo rápido, mientras que C/C++ ofrece un mayor rendimiento y un control más directo sobre el hardware.

En conclusión, la ESP32 es una herramienta adecuada tanto para estudiantes que están comenzando en el área de los sistemas embebidos como para el desarrollo de prototipos y aplicaciones de automatización, robótica e Internet de las Cosas.

---

# 22. Estructura recomendada del repositorio

Para que las imágenes funcionen correctamente en GitHub, el repositorio puede organizarse de la siguiente manera:

```text
Proyecto-ESP32/
│
├── README.md
│
├── Imagenes/
│   ├── ESP32.jpg
│   ├── ESP-WROOM-32.jpg
│   ├── Arquitectura_ESP32.jpg
│   └── Pinout_ESP32.png
│
└── Codigos/
    ├── LED_Arduino.ino
    ├── ADC_ESP32.ino
    ├── PWM_ESP32.ino
    └── LED_MicroPython.py
```

---

# 23. Comandos para insertar imágenes en GitHub

Para llamar una imagen desde el archivo `README.md`, se utiliza la siguiente estructura:

```markdown
![Descripción de la imagen](./Imagenes/nombre_de_la_imagen.jpg)
```

Por ejemplo:

```markdown
![Placa ESP32](./Imagenes/ESP32.jpg)
```

Si se desea agregar un texto debajo de la imagen:

```markdown
![Placa ESP32](./Imagenes/ESP32.jpg)

*Figura 1. Placa de desarrollo ESP32.*
```

Para una imagen PNG:

```markdown
![Pinout ESP32](./Imagenes/Pinout_ESP32.png)
```

Para una imagen centrada y con un tamaño determinado se puede utilizar HTML dentro del archivo Markdown:

```html
<p align="center">
  <img src="./Imagenes/ESP32.jpg" alt="Placa ESP32" width="500">
</p>
```

También es posible agregar una descripción:

```html
<p align="center">
  <img src="./Imagenes/ESP32.jpg" alt="Placa ESP32" width="500">
</p>

<p align="center">
  <i>Figura 1. Placa de desarrollo basada en ESP-WROOM-32.</i>
</p>
```

---

## Autor

**Fabian**

Proyecto académico sobre la placa **ESP-WROOM-32 / ESP32**.

