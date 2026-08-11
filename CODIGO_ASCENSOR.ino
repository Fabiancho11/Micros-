#define REMOTEXY__DEBUGLOG    
#define REMOTEXY_MODE__WIFI_POINT
// ================= LIBRERIAS =================
#include <WiFi.h>
#include <RemoteXY.h>
#include <SPI.h>
#include <MFRC522.h>

// ================= WIFI =================
#define REMOTEXY_WIFI_SSID "RemoteXY"
#define REMOTEXY_WIFI_PASSWORD "12345678"
#define REMOTEXY_SERVER_PORT 6377

// ================= RFID =================
#define SS_PIN 5
#define RST_PIN 22
MFRC522 rfid(SS_PIN, RST_PIN);

byte uidsPermitidos[5][4] = {
  {0xBA, 0xAA, 0x25, 0x31},
  {0x1A, 0xB7, 0x4F, 0x31},
  {0x4A, 0x5D, 0x3E, 0x31},
  {0x2A, 0x7B, 0x47, 0x31},
  {0xBA, 0x16, 0x49, 0x31}
};

bool acceso = false;

// ================= MOTORES =================
#define IN1 25
#define IN2 26
#define ENA 4

#define IN3 27
#define IN4 14
#define ENB 16

// ================= SENSORES =================
#define PISO1 33
#define PISO2 32
#define PISO3 35
#define PISO4 34
#define BTN_FRENAR 17

// ================= CONTROL =================
int destino = 0;
bool moviendo = false;
int ultimoPiso = 0;

// motor B
unsigned long tiempoMotorB = 0;
bool motorBActivo = false;

// flancos
bool last_p1=0, last_p2=0, last_p3=0, last_p4=0;
bool last_e=0, last_r=0;

unsigned long tiempoLED = 0;
bool ledActivo = false;
bool last_frenar = HIGH;

bool bajarDespuesDeE = false;
unsigned long tiempoBajada = 0;

bool subirPrimeroR = false;
bool enSecuenciaE = false;
bool enSecuenciaR = false;
bool modoSecuencia = false;
bool listoParaBajar = false;
unsigned long tiempoInicioBajadaA = 0;
bool bajandoA = false;
unsigned long duracionMotorB = 0;

// ================= INTERFAZ =================
#pragma pack(push, 1)  
uint8_t const PROGMEM RemoteXY_CONF_PROGMEM[] = {
  255,9,0,17,0,74,1,19,0,0,0,0,31,1,106,200,1,1,24,0,
  1,11,17,21,21,0,0,31,52,0,70,36,23,8,8,16,26,134,0,70,
  35,138,9,9,16,26,37,0,1,6,162,24,24,0,6,31,66,65,74,65,
  82,0,1,39,162,24,24,0,6,31,83,85,66,73,82,0,1,66,73,24,
  24,0,134,31,69,78,84,82,69,71,65,82,0,1,66,102,24,24,0,134,
  31,82,69,67,79,71,69,82,0,70,83,20,14,14,16,26,37,0,70,83,
  40,14,14,16,26,134,0,69,61,20,15,15,0,1,69,62,39,15,15,0,
  134,70,20,138,9,9,16,26,134,0,74,6,8,51,5,0,16,24,64,83,
  69,76,69,67,67,73,79,78,32,68,69,32,80,73,83,79,0,1,11,44,
  21,21,0,0,31,51,0,70,36,52,8,8,16,26,134,0,1,11,71,21,
  21,0,0,31,50,0,70,36,77,8,8,16,26,134,0,1,11,98,21,21,
  0,0,31,49,0,70,36,104,8,8,16,26,134,0,74,69,11,51,5,0,
  16,24,64,65,67,67,69,83,79,0,74,66,64,51,5,0,16,24,64,65,
  67,67,73,79,78,69,83,0,74,7,129,54,5,0,16,24,64,69,83,84,
  65,68,79,32,68,69,76,32,83,73,83,84,69,77,65,0,74,11,154,54,
  5,0,16,24,64,67,79,78,84,82,79,76,32,77,65,78,85,65,76,0,
  10,71,161,24,24,48,17,26,31,79,78,0,31,79,70,70,0 
  };

struct {
  uint8_t piso_4;
  uint8_t b;
  uint8_t s;
  uint8_t e;
  uint8_t r;
  uint8_t piso_3;
  uint8_t piso_2;
  uint8_t piso_1;
  uint8_t control_manual;

  uint8_t led_piso4;
  uint8_t inactivo;
  uint8_t led_acceso_denegado;
  uint8_t led_acceso_concedido;
  int16_t sound_01;
  int16_t sound_02;
  uint8_t activo;
  uint8_t strings_05;
  uint8_t led_piso3;
  uint8_t led_piso2;
  uint8_t led_piso1;
  uint8_t strings_01;
  uint8_t strings_02;
  uint8_t strings_03;
  uint8_t strings_04;

  uint8_t connect_flag; 
} RemoteXY;
#pragma pack(pop)

// ================= FUNCIONES =================
int pisoActual() {
  if (digitalRead(PISO1)) return 1;
  if (digitalRead(PISO2)) return 2;
  if (digitalRead(PISO3)) return 3;
  if (digitalRead(PISO4)) return 4;
  return 0;
}

void detenerMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  moviendo = false;
  destino = 0;
}

void iniciarMovimiento(int dest) {
  if (!acceso) return;
  int actual = pisoActual();
  if (actual == dest) return;
  destino = dest;
  if (actual < destino) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
  } else {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
  }
  moviendo = true;
}

void setup() {
  RemoteXY_Init();
  RemoteXY.strings_05 = 1;
  RemoteXY.strings_01 = 1;
  RemoteXY.strings_02 = 1;
  RemoteXY.strings_03 = 1;
  RemoteXY.strings_04 = 1;

  SPI.begin();
  rfid.PCD_Init();

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  digitalWrite(ENA, HIGH);
  digitalWrite(ENB, HIGH);

  pinMode(PISO1, INPUT);
  pinMode(PISO2, INPUT);
  pinMode(PISO3, INPUT);
  pinMode(PISO4, INPUT);
  pinMode(BTN_FRENAR, INPUT_PULLUP);
}

void loop() {
  RemoteXY_Handler();

  // ===== RFID =====
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    bool coincide = false;
    for (byte j = 0; j < 5; j++) {
      bool igual = true;
      for (byte i = 0; i < 4; i++) {
        if (rfid.uid.uidByte[i] != uidsPermitidos[j][i]) {
          igual = false;
          break;
        }
      }
      if (igual) {
        coincide = true;
        break;
      }
    }
    if (coincide) {
      acceso = true;
      RemoteXY.led_acceso_concedido = 1;
      RemoteXY.led_acceso_denegado = 0;
      tiempoLED = millis();
      ledActivo = true;
    } else {
      acceso = false;
      RemoteXY.led_acceso_concedido = 0;
      RemoteXY.led_acceso_denegado = 1;
      tiempoLED = millis();
      ledActivo = true;
    }
  }

  if (ledActivo && millis() - tiempoLED >= 200) {
    RemoteXY.led_acceso_concedido = 0;
    RemoteXY.led_acceso_denegado = 0;
    ledActivo = false;
  }

  int actual = pisoActual();

  if (!acceso) {
    detenerMotor();
    RemoteXY.activo = 0;
    RemoteXY.inactivo = 1;
    return;
  }

  if (RemoteXY.control_manual) {
    modoSecuencia = false;
    bajarDespuesDeE = false;
    subirPrimeroR = false;
    motorBActivo = false;
  }

  // ===== ESTADO =====
  if (!acceso) {
    RemoteXY.activo = 0;
    RemoteXY.inactivo = 1;
  } else {
    if (!moviendo && actual == 0) {
      RemoteXY.activo = 0;
      RemoteXY.inactivo = 1;
    } else {
      RemoteXY.activo = 1;
      RemoteXY.inactivo = 0;
    }
  }

  // ===== LEDS PISOS =====
  RemoteXY.led_piso1 = (actual == 1);
  RemoteXY.led_piso2 = (actual == 2);
  RemoteXY.led_piso3 = (actual == 3);
  RemoteXY.led_piso4 = (actual == 4);

  // ===== BOTONES PISOS =====
  if (acceso && !RemoteXY.control_manual) { 
    if (RemoteXY.piso_1 && !last_p1) iniciarMovimiento(1);
    if (RemoteXY.piso_2 && !last_p2) iniciarMovimiento(2);
    if (RemoteXY.piso_3 && !last_p3) iniciarMovimiento(3);
    if (RemoteXY.piso_4 && !last_p4) iniciarMovimiento(4);
  }

  last_p1 = RemoteXY.piso_1;
  last_p2 = RemoteXY.piso_2;
  last_p3 = RemoteXY.piso_3;
  last_p4 = RemoteXY.piso_4;

  // ===== BOTONES E y R (AUTOMÁTICO) =====
  if (!RemoteXY.control_manual && acceso) {
    if (RemoteXY.e && !last_e) {
      modoSecuencia = true;
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      tiempoMotorB = millis();
      motorBActivo = true;
      duracionMotorB = 600;
      bajarDespuesDeE = true;
      listoParaBajar = false;
    }
    if (RemoteXY.r && !last_r) {
      modoSecuencia = true;
      subirPrimeroR = true;
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      moviendo = true;
    }
  }

  // ===== SECUENCIA R (sube → luego motor B) =====
  if (subirPrimeroR && moviendo) {
    if (digitalRead(PISO1) || digitalRead(PISO2) || digitalRead(PISO3) || digitalRead(PISO4)) {
      detenerMotor();
      subirPrimeroR = false;
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      tiempoMotorB = millis();
      motorBActivo = true;
      duracionMotorB = 800; 
    }
  }

  last_e = RemoteXY.e;
  last_r = RemoteXY.r;

  // ===== LÓGICA MOTOR B =====
  if (motorBActivo && millis() - tiempoMotorB >= duracionMotorB) {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    motorBActivo = false;
    if (bajarDespuesDeE) {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      moviendo = true;
      bajandoA = true;
      tiempoInicioBajadaA = millis();
      modoSecuencia = false;
      bajarDespuesDeE = false;
    }
  }

  // ===== FINALIZAR BAJADA TRAS E =====
if (bajandoA) {
  int piso = pisoActual();

  if (
    (piso == 4 && millis() - tiempoInicioBajadaA >= 25) ||
    (piso == 3 && millis() - tiempoInicioBajadaA >= 50) ||
    (piso == 2 && millis() - tiempoInicioBajadaA >= 180) ||
    (piso <= 1 && millis() - tiempoInicioBajadaA >= 150)
  ) {
    detenerMotor();
    bajandoA = false;
  }
}

  // ===== CONTROL DE LLEGADA A DESTINO =====
  if (moviendo && !bajandoA && !subirPrimeroR) {
    if (destino == 1 && digitalRead(PISO1)) detenerMotor();
    if (destino == 2 && digitalRead(PISO2)) detenerMotor();
    if (destino == 3 && digitalRead(PISO3)) detenerMotor();
    if (destino == 4 && digitalRead(PISO4)) detenerMotor();
  }

  // ===== CONTROL MANUAL =====
  if (RemoteXY.control_manual && acceso) {
    if (RemoteXY.s) {
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      moviendo = false;
    } else if (RemoteXY.b) {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      moviendo = false;
    } else {
      detenerMotor();
    }
  } 

  // ===== BOTÓN DE EMERGENCIA (FRENAR) =====
  bool estadoFrenar = digitalRead(BTN_FRENAR);
  if (last_frenar == HIGH && estadoFrenar == LOW) {
    detenerMotor();
    acceso = false;
    RemoteXY.led_acceso_concedido = 0;
    RemoteXY.led_acceso_denegado = 0;
    RemoteXY.activo = 0;
    RemoteXY.inactivo = 1;
  }
  last_frenar = estadoFrenar;

  RemoteXY_delay(10);
}
