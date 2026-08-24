<h1 align="center">ESP-WROOM-32</h1>

<p>La ESP-32 es un microcontrolador desarrollado para aplicaciones de electrónica, automatización, robótica e Internet de las Cosas (IoT). Se caracteriza por integrar conectividad <strong>Wi-Fi y Bluetooth</strong> además de diferentes periféricos para la conexión de sensores y actuadores.</p>

<h2>Estructura y arquitectura</h2>

<p>La ESP-32 posee una arquitectura basada en un microprocesador <strong>Xtensa Dual-Core de 32 bits LX6</strong>, memoria interna, conectividad inalámbrica y múltiples periféricos. Su estructura está compuesta principalmente por el procesador, memoria Flash (típicamente de 4 MB), memoria SRAM (520 KB), memoria ROM (448 KB), módulos Wi-Fi y Bluetooth, pines GPIO y sistemas de comunicación.</p>

<p>A continuación, se muestra el diagrama de bloques de este microcontrolador:</p>

<div align="center">
  <img src="../Imagenes/diagrama.jpg" alt="Diagrama de bloques funcionales de la ESP32">
</div>

<h2>Características de la ESP32</h2>

<p>Caracteristicas:</p>

<ul>
  <li><strong>Procesador:</strong> Microprocesador Xtensa Dual-Core 32-bit LX6 (frecuencia hasta 240 MHz).</li>
  <li><strong>Memoria:</strong> 
    <ul>
      <li><strong>SRAM:</strong> 520 KB para datos e instrucciones.</li>
      <li><strong>ROM:</strong> 448 KB para el arranque y funciones del núcleo.</li>
      <li><strong>Flash SPI:</strong> Típicamente de 4 MB utilizada para almacenar el código y datos.</li>
    </ul>
  </li>
  <li><strong>Conectividad:</strong> Wi-Fi (802.11 b/g/n) y Bluetooth (v4.2 BR/EDR y BLE).</li>
    <ul>
      <li>Múltiples pines GPIO.</li>
    </ul>
  </li>
  <li><strong>Eficiencia:</strong> Bajo consumo de energía.</li>
</ul>

<h2>Conexiones y pines:</h2>

<p>Los GPIOS(Entrada/Salida de Propósito General) permiten interactuar con diferentes componentes sensores, leds, actuadores y pantallas. Dependiendo de su configuración, pueden funcionar como entradas, salidas o cumplir funciones específicas.</p>

<div align="center">
  <img src="../Imagenes/ESP32.jpg" alt="Diagrama de pines de la ESP32">
</div>

<h2>ADC</h2>

<p>El <strong>ADC (Conversor Analógico-Digital)</strong> permite convertir señales analógicas en valores digitales. Esta función es utilizada para la lectura de sensores como potenciómetros, LDR y sensores analógicos de temperatura.</p>

<h2>PWM</h2>

<p>El <strong>PWM (Modulación por Ancho de Pulso)</strong> permite generar señales con un ciclo de trabajo variable. Se utiliza principalmente para controlar el brillo de LEDs, la velocidad de motores y la angulo de servomotores.</p>

<h2>DAC</h2>

<p>El <strong>DAC (Conversor Digital-Analógico)</strong> permite generar una señal analógica a partir de un valor digital. Algo curioso es que para realizar esta accion se requiere un circuito en especifico por lo cual la ESP-32 solo tiene dos pines que generan un voltaje variable real el GPIO 25 Y 26.</p>

| Tecnología | Ventajas | Desventajas |
|---|---|---|
| **MicroPython** | - Prototipado rápido.<br>- Sintaxis sencilla.<br>- Pruebas en tiempo real mediante REPL. | - Menor velocidad de ejecución.<br>- Menor control del hardware a bajo nivel. |
| **C/C++** | - Mayor velocidad de ejecución.<br>- Mayor control del hardware.<br>- Adecuado para proyectos complejos. | - Mayor complejidad de aprendizaje.<br>- Mayor tiempo de desarrollo. |
