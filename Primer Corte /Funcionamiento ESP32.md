# Guía Completa de la ESP32: El Microcontrolador IoT Definitivo

Bienvenido a esta guía detallada sobre la **ESP32**, una potente familia de microcontroladores de bajo costo y bajo consumo de energía con Wi-Fi y Bluetooth de modo dual integrados. Desarrollado por Espressif Systems, es el sucesor del popular ESP8266 y se ha convertido en la base de innumerables proyectos de Internet de las Cosas (IoT).

![Vista general de una placa de desarrollo ESP32](./Imagenes/ESP32.jpg)
*Imagen: Una placa de desarrollo ESP32 estándar.*

## ¿Qué es y Para Qué Sirve?

La ESP32 no es solo un microcontrolador básico; es un sistema en un chip (SoC). Su propósito principal es proporcionar conectividad inalámbrica robusta y una potencia de procesamiento considerable para una amplia gama de aplicaciones, desde sensores simples hasta sistemas de control complejos, todo en un paquete pequeño y asequible. Sirve para dar vida a proyectos que requieren comunicación con la nube, procesamiento de datos locales y control de hardware.

## Procesador y Rendimiento

El "cerebro" de la ESP32 es excepcionalmente potente en comparación con microcontroladores anteriores de su clase.

*   **Núcleos:** La mayoría de los módulos ESP32 cuentan con un procesador **dual-core** (dos núcleos). Esto permite realizar tareas en paralelo, como gestionar la conexión Wi-Fi en un núcleo mientras se lee un sensor y se ejecuta lógica compleja en el otro.
*   **Arquitectura:** Utiliza microprocesadores **Tensilica Xtensa LX6 de 32 bits**.
*   **Velocidad de Reloj:** Puede funcionar a frecuencias de hasta **240 MHz**.

## Memoria

La ESP32 tiene diferentes tipos de memoria diseñadas para propósitos específicos.

*   **ROM (Internal Read-Only Memory):** Contiene código fundamental que no cambia, como el gestor de arranque (bootloader) y funciones del sistema central. (Alrededor de 448 KB).
*   **Internal SRAM (Static Random-Access Memory):** Esta es la memoria de trabajo rápida donde se almacenan tus variables y datos mientras el programa se ejecuta. (Aproximadamente 520 KB disponibles para el usuario).
*   **External Flash Memory:** Aquí es donde se almacena permanentemente el código de tu programa (tu "sketch" de Arduino o script de MicroPython) y archivos. La mayoría de los módulos vienen con **4MB** de flash, pero pueden soportar hasta 16MB.

## Pines GPIO: Tipos y Funciones

Los pines GPIO (General Purpose Input/Output) son la interfaz física de la ESP32 para interactuar con el mundo exterior. Dependiendo de la placa de desarrollo, tendrás acceso a unos 30-40 pines útiles.

**Importante:** No todos los pines son iguales.

![Pinout completo de una placa ESP32 común](ruta/de/la/imagen_pinout_esp32.png)
*Imagen: Diagrama de distribución de pines (Pinout) de una placa ESP32 estándar. Nota: La disposición puede variar ligeramente según el fabricante.*

### Principales Funciones de los Pines GPIO

1.  **Entradas/Salidas Digitales:**
    *   Pueden leer o escribir estados lógicos (Alto/1 o Bajo/0). Usados para botones, LEDs, interruptores, etc. La mayoría de los pines GPIO tienen esta función básica.

2.  **ADC (Convertidores Analógico-Digital):**
    *   **Función:** Convierten señales de voltaje analógico (como las de un sensor de temperatura o potenciómetro) en números digitales que el procesador puede entender.
    *   **Detalles:** La ESP32 tiene múltiples canales ADC (hasta 18 en total en dos módulos ADC) con una alta resolución de hasta **12 bits** (valores de 0 a 4095).

3.  **DAC (Convertidores Digital-Analógico):**
    *   **Función:** Hacen lo contrario al ADC; convierten un número digital en un voltaje analógico real y suave.
    *   **Detalles:** Tiene **2 canales** de 8 bits (valores de 0 a 255), útiles para generar formas de onda simples o audio.

4.  **PWM (Modulación por Ancho de Pulso):**
    *   **Función:** Usada para controlar la potencia entregada a un dispositivo, como el brillo de un LED o la velocidad de un motor, mediante una señal digital que pulsa rápidamente.
    *   **Detalles:** La ESP32 tiene hardware dedicado para PWM, incluyendo un módulo de control LED y un módulo de control de motores, que permiten PWM flexible en casi cualquier pin GPIO.

5.  **Pines de Toque Capacitivo:**
    *   **Función:** Actúan como sensores de tacto sin necesidad de botones físicos.
    *   **Detalles:** Hay alrededor de **10 pines** que pueden detectar cambios en la capacitancia causados por el toque humano.

6.  **Interfaces de Comunicación:**
    *   **UART (Universal Asynchronous Receiver-Transmitter):** Tiene 3 puertos UART seriales para comunicarse con computadoras u otros módulos seriales (como GPS).
    *   **SPI (Serial Peripheral Interface):** Tiene 3 puertos SPI para comunicación rápida con sensores, pantallas y tarjetas SD.
    *   **I2C (Inter-Integrated Circuit):** Tiene 2 puertos I2C para conectar múltiples sensores y periféricos en solo dos cables.
    *   **I2S (Inter-IC Sound):** Para interfaces de audio digital.
    *   **CAN bus (TWAI):** Para aplicaciones de redes automotrices e industriales.

## Aplicaciones Principales

Gracias a su potencia y conectividad, la ESP32 es increíblemente versátil. Aquí tienes algunas de sus aplicaciones más comunes:

*   **Internet de las Cosas (IoT) Doméstica:** Termostatos inteligentes, enchufes controlados por Wi-Fi, iluminación inteligente, estaciones meteorológicas conectadas.
*   **Automatización Industrial:** Monitoreo de maquinaria, recolección de datos de sensores a gran escala, sistemas de control simplificados.
*   **Wearables (Dispositivos Vestibles):** Relojes inteligentes, rastreadores de actividad física que utilizan Bluetooth Low Energy (BLE) para comunicarse con teléfonos.
*   **Robótica:** Control de motores (usando PWM), procesamiento de datos de sensores (como LiDAR simples) y control remoto vía Wi-Fi o Bluetooth.
*   **Streaming de Audio/Video:** Debido a su potencia y módulos de audio/cámara, puede usarse para radios de internet o cámaras IP básicas.
*   **Prototipado Rápido y Educación:** Ideal para estudiantes y "makers" para crear rápidamente prototipos de ideas conectadas.

![Ejemplo de aplicación IoT: Monitoreo de una planta con ESP32](ruta/de/la/imagen_aplicacion_ejemplo.jpg)
*Imagen: Un ejemplo conceptual de la ESP32 utilizada para monitorear una planta, leyendo un sensor de humedad y enviando los datos a una plataforma en la nube via Wi-Fi.*

---

## Cómo Insertar tus Imágenes Reales en GitHub

Como mencioné, el código de arriba tiene marcadores de posición para las imágenes, como `ruta/de/la/imagen_esp32_general.jpg`. Ahora te explico cómo hacer que tus imágenes aparezcan allí:

### Paso 1: Sube tus imágenes a GitHub

1.  **Guarda tus imágenes:** Ten listos los archivos de imagen que quieras usar (formato JPG, PNG o GIF) en tu computadora. Usa nombres de archivo descriptivos (ej: `esp32_desarrollo.jpg`, `pinout_esp32.png`).
2.  **Crea una carpeta (Opcional pero Recomendado):** En la página de tu repositorio en GitHub, haz clic en **"Add file"** > **"Create new file"**. Escribe un nombre de carpeta seguido de una barra diagonal (ej: `imagenes/`) y luego el nombre de un archivo ficticio para crear la carpeta (ej: `imagenes/.gitkeep`). Luego puedes borrar ese archivo. Esto mantendrá tu proyecto organizado.
3.  **Sube las imágenes:** Ve a la carpeta que creaste (o a la raíz del repositorio), haz clic en **"Add file"** > **"Upload files"**. Arrastra y suelta todas tus imágenes allí.
4.  **Guarda los cambios (Commit):** Escribe un mensaje breve (ej: "Agregué imágenes para el README") y haz clic en el botón verde de guardar cambios.

### Paso 2: Obtén la ruta correcta y reemplaza los marcadores de posición

La forma más profesional y portátil de incluir imágenes en un repositorio de GitHub es usar **rutas relativas**. Esto significa que el código de la imagen apuntará a un archivo *dentro de tu propio repositorio*, en lugar de a un enlace externo de internet.

1.  **Edita tu `README.md`:** Abre tu archivo `README.md` en GitHub en el modo de edición (icono de lápiz ✏️).
2.  **Busca un marcador de posición de imagen:** Localiza una línea como `![Vista general...](ruta/de/la/imagen_esp32_general.jpg)`.
3.  **Reemplaza la ruta:** Sustituye el texto dentro de los paréntesis `ruta/de/la/imagen_esp32_general.jpg` con la ruta relativa real a tu imagen.
    *   **Si la imagen está en la misma carpeta que el `README.md`:** Simplemente pon el nombre del archivo. Ej: `![Vista general...](esp32_desarrollo.jpg)`.
    *   **Si la imagen está en una carpeta llamada `imagenes`:** Pon `./nombre_carpeta/nombre_archivo`. Ej: `![Vista general...](./imagenes/esp32_desarrollo.jpg)`. (El `./` indica "comenzar en la carpeta actual").
4.  **Repite para todas las imágenes.**
5.  **Revisa la vista previa:** Haz clic en la pestaña **"Preview"** para asegurarte de que todas tus imágenes se cargan correctamente y se ven como esperas.
6.  **Guarda tus cambios (Commit):** Cuando estés satisfecho, guarda los cambios de tu `README.md`.

¡Y listo! Tu página quedará guardada y se verá muy profesional con toda la explicación y tus imágenes integradas.
