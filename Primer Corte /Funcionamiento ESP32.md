# **ESP-WROOM-32 - Características y Programación**

La **ESP-WROOM-32** es un módulo basado en el microcontrolador **ESP32**, desarrollado para aplicaciones de electrónica, automatización, robótica e Internet de las Cosas (IoT). Se caracteriza por integrar conectividad **Wi-Fi y Bluetooth**, además de diferentes periféricos para la conexión de sensores y actuadores.

## Definición, estructura y arquitectura

La ESP-WROOM-32 posee una arquitectura basada en un procesador de **32 bits**, memoria interna, conectividad inalámbrica y múltiples periféricos. Su estructura está compuesta principalmente por el procesador, memoria Flash, memoria RAM, módulos Wi-Fi y Bluetooth, pines GPIO y sistemas de comunicación.

## Características de la ESP32

Entre sus principales características se encuentran:

- Procesador de 32 bits.
- Conectividad Wi-Fi y Bluetooth.
- Múltiples pines GPIO.
- Entradas analógicas ADC.
- Salidas PWM.
- Conversores DAC.
- Comunicación UART, SPI e I2C.
- Bajo consumo de energía.

## Conexiones y pines

Los pines GPIO de la ESP32 permiten conectar diferentes dispositivos electrónicos, como sensores, LEDs, motores y pantallas. Dependiendo de su configuración, pueden funcionar como entradas, salidas o cumplir funciones específicas.

![Pinout ESP32](Imagenes/ESP32.jpg)

## ADC

El **ADC (Conversor Analógico-Digital)** permite convertir señales analógicas en valores digitales. Esta función es utilizada para la lectura de sensores como potenciómetros, LDR y sensores analógicos de temperatura.

## PWM

La **PWM (Modulación por Ancho de Pulso)** permite generar señales con un ciclo de trabajo variable. Se utiliza principalmente para controlar el brillo de LEDs, la velocidad de motores y la posición de servomotores.

## DAC

El **DAC (Conversor Digital-Analógico)** permite generar una señal analógica a partir de un valor digital. En la ESP32 clásica, las salidas DAC se encuentran principalmente en:

- GPIO 25.
- GPIO 26.

## Programación en C/C++

### Ventajas

- Mayor velocidad de ejecución.
- Mayor control sobre el hardware.
- Amplio soporte de librerías.
- Adecuado para proyectos complejos.

### Desventajas

- Mayor dificultad de aprendizaje.
- Código más extenso.
- Requiere mayor conocimiento de programación.

## Programación en MicroPython

### Ventajas

- Sintaxis sencilla y fácil de aprender.
- Desarrollo rápido de programas.
- Ideal para proyectos educativos y prototipos.
- Permite realizar pruebas de forma rápida.

### Desventajas

- Menor velocidad de ejecución que C/C++.
- Mayor consumo de memoria.
- Algunas librerías y funciones pueden tener soporte limitado.
