# Sistema de Detección e Identificación de Juguetes con YOLOv8 y ESP32

Este laboratorio aborda el desarrollo de un sistema de visión artificial en tiempo real integrado con sistemas embebidos, dando cumplimiento a los requerimientos planteados para la práctica de detección de objetos y control físico.

---

## 📋 Requerimientos del Laboratorio

De acuerdo con la guía de la práctica, los objetivos desarrollados en este repositorio son:

1. **Desarrollo en Wokwi (MicroPython):** Implementación del esquema de prueba que simula el control de los LEDs mediante lectura de comandos/entradas físicas en la tarjeta ESP32.
2. **Revisión de Arquitectura YOLO:** Análisis y comprensión del funcionamiento del modelo de visión artificial basado en la arquitectura YOLOv8.
3. **Integración Hardware - Visión Artificial:** Detección en tiempo real de carros y motos de juguete mediante webcam. Al detectar un **carro de juguete**, la ESP32 enciende el **LED rojo**; al detectar una **moto de juguete**, se enciende el **LED verde**.

![Esquema Wokwi](Imagenes/esquema_wokwi.png)

---

## 🧠 Entrenamiento del Modelo en Google Colab (YOLOv8)

Para lograr una clasificación precisa entre carros y motos de juguete, se llevó a cabo un proceso de *Fine-Tuning* sobre la arquitectura **YOLOv8 Nano**.

### Dataset (Roboflow)
El dataset fue obtenido y procesado desde Roboflow para asegurar un correcto balance de clases y diversidad de ángulos:
* **Clase Moto:** 1,498 imágenes.
* **Clase Carro:** 1,096 imágenes.

### Proceso de Entrenamiento
Debido a la alta demanda computacional y al volumen de imágenes, el modelo requirió un tiempo de ejecución continuo de **40 minutos**. Por este motivo, el entrenamiento se realizó en la plataforma **Google Colab** aprovechando su aceleración por hardware (GPU T4), evitando cuellos de botella en equipos locales.

### Código de Entrenamiento utilizado en Google Colab
<!-- PEGA AQUÍ TU CÓDIGO DE COLAB -->
```python
# [CÓDIGO DE ENTRENAMIENTO EN COLAB]
