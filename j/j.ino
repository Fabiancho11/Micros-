#include <Adafruit_NeoPixel.h>

#define PIN_RGB     48
#define NUM_PIXELS  1

Adafruit_NeoPixel rgb(NUM_PIXELS, PIN_RGB, NEO_GRB + NEO_KHZ800);

// Función para mostrar un color
void mostrarColor(uint8_t r, uint8_t g, uint8_t b)
{
  rgb.setPixelColor(0, rgb.Color(r, g, b));
  rgb.show();
}

void setup()
{
  rgb.begin();
  rgb.setBrightness(100);   // Brillo (0-255)
}

void loop()
{
  // Blanco
  mostrarColor(255, 255, 255);
  delay(1000);

  // Amarillo
  mostrarColor(255, 255, 0);
  delay(1000);

  // Cian
  mostrarColor(0, 255, 255);
  delay(1000);

  // Magenta
  mostrarColor(255, 0, 255);
  delay(1000);

  // Azul personalizado (#00FCFF)
  mostrarColor(0, 252, 255);
  delay(1000);
}