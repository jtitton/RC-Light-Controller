/*
 * ============================================================
 *  Sistema de Luzes para Carro RC - v5.1
 *  Arduino Nano + Receptor FS-BS6
 *  Pinagem compatível com luzesbronco v3.8
 * ============================================================
 *
 * Entradas (Servo PPM do receptor):
 *   D4 - Direção do volante  (CH1, Pin Change Interrupt PCINT20)
 *   D2 - Aceleração          (CH2, Interrupção externa INT0)
 *   D3 - Farol               (CH4, Interrupção externa INT1)
 *
 * Saídas (LEDs):
 *   D5  - Lanterna traseira  (vermelho, PWM, com fade)
 *   D6  - Luz de freio       (vermelho, Digital/PWM)
 *   D9  - Farol dianteiro    (branco, PWM)
 *   D10 - Pisca esquerdo     (laranja, Digital)
 *   D11 - Pisca direito      (laranja, Digital)
 *
 * Melhorias v5.1:
 *   - Lógica 100% interrupt-driven (sem pulseIn bloqueante)
 *   - PCINT20 no pino D4 para leitura do volante sem bloqueio
 *   - Média móvel atualizada apenas na recepção de novos pulsos
 *   - Protótipos de funções incluídos para evitar erros de compilação
 *   - Transições de fade ultra-suaves devido ao loop sem bloqueio (~40000Hz)
 */

#include <EEPROM.h>

// ============================================================
// PINAGEM (compatível com luzesbronco v3.8)
// ============================================================
#define PIN_IN_STEERING    4    // CH1 - Volante (PCINT20)
#define PIN_IN_THROTTLE    2    // CH2 - Aceleração (INT0)
#define PIN_IN_HEADLIGHT   3    // CH4 - Farol (INT1)

#define PIN_OUT_TAIL       5    // PWM - Lanterna traseira
#define PIN_OUT_BRAKE      6    // PWM/Digital - Luz de freio
#define PIN_OUT_HEADLIGHT  9    // PWM - Farol dianteiro
#define PIN_OUT_BLINK_L    10   // Pisca esquerdo
#define PIN_OUT_BLINK_R    11   // Pisca direito

// ============================================================
// CONSTANTES
// ============================================================
#define EEPROM_MAGIC_VALUE  0xAD
#define EEPROM_START_ADDR   0

#define PPM_VALID_MIN       800
#define PPM_VALID_MAX       2200

#define DEFAULT_CENTER      1500
#define DEFAULT_DEFLECTION  500

// --- Limiares em Percentual ---
#define STEERING_BLINK_PERCENT   70
#define THROTTLE_BRAKE_PERCENT   5
#define HEADLIGHT_THRESH_LOW     33
#define HEADLIGHT_THRESH_HIGH    66

// --- Brilho ---
#define BRIGHTNESS_OFF           0
#define BRIGHTNESS_40            102
#define BRIGHTNESS_100           255

// --- Pisca ---
#define BLINK_INTERVAL_MS        250   // 250ms on / 250ms off (120 piscadas/minuto, ajustado)

// --- Fade (lanterna traseira) ---
#define FADE_STEP_INTERVAL_MS    6     // Atualiza a cada ~6ms
#define FADE_STEP_SIZE           5     // Incremento por passo
// Transição 0 -> 255: ~51 passos x 6ms = ~306ms

// --- Filtro de média móvel ---
#define FILTER_SIZE              5

// --- Timing ---
#define AUTOCENTER_DURATION_MS   2000
#define CAL_EXTREMES_DURATION_MS 5000
#define CAL_HEADLIGHT_DURATION_MS 5000
#define CAL_MIN_RANGE            200
#define DEBUG_INTERVAL_MS        500
#define SERIAL_BAUD              115200

// ============================================================
// ESTRUTURAS
// ============================================================
struct CalibrationData {
  uint8_t magic;
  int steerDeflLeft;
  int steerDeflRight;
  int throDeflBack;
  int throDeflFwd;
  int headlightMin;
  int headlightMax;
};

struct MovingAvgFilter {
  int samples[FILTER_SIZE];
  int index;

  void init(int defaultVal) {
    for (int i = 0; i < FILTER_SIZE; i++) samples[i] = defaultVal;
    index = 0;
  }

  int update(int newValue) {
    samples[index] = newValue;
    index = (index + 1) % FILTER_SIZE;
    return average();
  }

  int average() const {
    long sum = 0;
    for (int i = 0; i < FILTER_SIZE; i++) sum += samples[i];
    return (int)(sum / FILTER_SIZE);
  }
};

enum HeadlightMode { HL_OFF, HL_DIM, HL_FULL };

enum BlinkDirection {
  BLINK_LEFT  = -1,
  BLINK_NONE  =  0,
  BLINK_RIGHT =  1
};

// ============================================================
// PROTÓTIPOS DE FUNÇÕES
// ============================================================
void throttleISR();
void headlightISR();
int steeringToPercent(int ppm);
int throttleToPercent(int ppm);
int headlightToPercent(int ppm);
void allLEDsOff();
void blinkAllLEDs(int count, int intervalMs);
bool loadCalibration();
void saveCalibration();
void resetEEPROM();
void printCalibration();
void autoCenter();
void runFullCalibration();
int getFilteredSteering();
int getFilteredThrottle();
int getFilteredHeadlight();
HeadlightMode calcHeadlightMode(int hlPercent);
bool isBraking(int throPct);
BlinkDirection getBlinkDirection(int steerPct);
void updateHeadlight(HeadlightMode mode);
void setTailLightTarget(HeadlightMode hlMode, bool braking);
void updateTailLightFade();
void updateBrakeLight(bool braking);
void updateBlinkers(BlinkDirection direction);
void processSerialCommand();

// ============================================================
// VARIÁVEIS GLOBAIS
// ============================================================

// --- Calibração (EEPROM) ---
CalibrationData g_cal;

// --- Centro detectado no boot ---
int g_steerCenter = DEFAULT_CENTER;
int g_throCenter  = DEFAULT_CENTER;

// --- ISR (Steering via PCINT, Throttle via INT0, Headlight via INT1) ---
volatile unsigned long g_steerRiseTime = 0;
volatile unsigned long g_throRiseTime  = 0;
volatile unsigned long g_hlRiseTime    = 0;

volatile int g_steerPulse = DEFAULT_CENTER;
volatile int g_throPulse  = DEFAULT_CENTER;
volatile int g_hlPulse    = DEFAULT_CENTER;

volatile bool g_steerNewPulse = false;
volatile bool g_throNewPulse  = false;
volatile bool g_hlNewPulse    = false;

// --- Filtros de média móvel ---
MovingAvgFilter g_steerFilter;
MovingAvgFilter g_throFilter;
MovingAvgFilter g_hlFilter;

// --- Fade (lanterna traseira) ---
int           g_tailCurrent = 0;    // Brilho atual (0-255)
int           g_tailTarget  = 0;    // Brilho alvo  (0-255)
unsigned long g_lastFadeUpdate = 0;

// --- Estado pisca ---
unsigned long g_lastBlinkToggle = 0;
bool          g_blinkState      = false;

// --- Estado farol ---
HeadlightMode g_hlMode = HL_OFF;

// ============================================================
// INTERRUPÇÕES (ISRs)
// ============================================================

// ISR para o pino D4 (Pin Change Interrupt PCINT2)
ISR(PCINT2_vect) {
  // PIND & (1 << 4) verifica o estado do pino D4 de forma ultra-rápida
  if (PIND & (1 << PIN_IN_STEERING)) {
    g_steerRiseTime = micros();
  } else {
    unsigned long pw = micros() - g_steerRiseTime;
    if (pw >= PPM_VALID_MIN && pw <= PPM_VALID_MAX) {
      g_steerPulse = (int)pw;
      g_steerNewPulse = true;
    }
  }
}

// ISR para o pino D2 (External Interrupt INT0)
void throttleISR() {
  if (PIND & (1 << PIN_IN_THROTTLE)) {
    g_throRiseTime = micros();
  } else {
    unsigned long pw = micros() - g_throRiseTime;
    if (pw >= PPM_VALID_MIN && pw <= PPM_VALID_MAX) {
      g_throPulse = (int)pw;
      g_throNewPulse = true;
    }
  }
}

// ISR para o pino D3 (External Interrupt INT1)
void headlightISR() {
  if (PIND & (1 << PIN_IN_HEADLIGHT)) {
    g_hlRiseTime = micros();
  } else {
    unsigned long pw = micros() - g_hlRiseTime;
    if (pw >= PPM_VALID_MIN && pw <= PPM_VALID_MAX) {
      g_hlPulse = (int)pw;
      g_hlNewPulse = true;
    }
  }
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  // Configura entradas
  pinMode(PIN_IN_STEERING,  INPUT);
  pinMode(PIN_IN_THROTTLE,  INPUT);
  pinMode(PIN_IN_HEADLIGHT, INPUT);

  // Configura saídas
  pinMode(PIN_OUT_TAIL,      OUTPUT);
  pinMode(PIN_OUT_BRAKE,     OUTPUT);
  pinMode(PIN_OUT_HEADLIGHT, OUTPUT);
  pinMode(PIN_OUT_BLINK_L,   OUTPUT);
  pinMode(PIN_OUT_BLINK_R,   OUTPUT);

  allLEDsOff();

  // Inicializa filtros de média móvel
  g_steerFilter.init(DEFAULT_CENTER);
  g_throFilter.init(DEFAULT_CENTER);
  g_hlFilter.init(DEFAULT_CENTER);

  // Inicializa a Serial
  Serial.begin(SERIAL_BAUD);
  Serial.println(F("\n==================================="));
  Serial.println(F(" Sistema de Luzes RC - v5.1"));
  Serial.println(F(" 100% Interrupt-driven (Não-bloqueante)"));
  Serial.println(F("==================================="));
  Serial.println(F(" C=Calibrar A=Centro P=Print ?=Ajuda\n"));

  // Configura e habilita as interrupções
  // 1. Pin Change Interrupt no pino D4 (PCINT20)
  PCICR |= (1 << PCIE2);      // Habilita PCINT para Port D (D0-D7)
  PCMSK2 |= (1 << PCINT20);   // Habilita interrupção específica para o pino D4 (PCINT20)

  // 2. Interrupções externas nos pinos D2 (INT0) e D3 (INT1)
  attachInterrupt(digitalPinToInterrupt(PIN_IN_THROTTLE),  throttleISR,  CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_IN_HEADLIGHT), headlightISR, CHANGE);

  // Executa o auto-centro baseado nas primeiras leituras de interrupção
  autoCenter();

  // Carrega calibração ou inicia a primeira calibração
  if (loadCalibration()) {
    Serial.println(F("\n✓ Calibração carregada da EEPROM."));
    printCalibration();
  } else {
    Serial.println(F("\n⚠ Sem calibração válida na EEPROM. Iniciando..."));
    g_cal.steerDeflLeft  = DEFAULT_DEFLECTION;
    g_cal.steerDeflRight = DEFAULT_DEFLECTION;
    g_cal.throDeflBack   = DEFAULT_DEFLECTION;
    g_cal.throDeflFwd    = DEFAULT_DEFLECTION;
    g_cal.headlightMin   = DEFAULT_CENTER - DEFAULT_DEFLECTION;
    g_cal.headlightMax   = DEFAULT_CENTER + DEFAULT_DEFLECTION;
    runFullCalibration();
  }

  Serial.println(F("Pronto! Boa pilotagem.\n"));
}

// ============================================================
// LOOP PRINCIPAL
// ============================================================
void loop() {
  // 1. Processa comandos enviados via Serial
  processSerialCommand();

  // 2. Lê valores suavizados do receptor (via ISR + Média Móvel)
  int steerRaw = getFilteredSteering();
  int throRaw  = getFilteredThrottle();
  int hlRaw    = getFilteredHeadlight();

  // 3. Converte os tempos de pulso (µs) para valores percentuais (-100% a +100%)
  int steerPct = steeringToPercent(steerRaw);
  int throPct  = throttleToPercent(throRaw);
  int hlPct    = headlightToPercent(hlRaw);

  // 4. Processa a lógica de controle
  g_hlMode = calcHeadlightMode(hlPct);
  bool           braking  = isBraking(throPct);
  BlinkDirection blinkDir = getBlinkDirection(steerPct);

  // 5. Atualiza o estado físico das saídas
  updateHeadlight(g_hlMode);
  setTailLightTarget(g_hlMode, braking);
  updateTailLightFade(); // Executado suavemente a cada ciclo
  updateBrakeLight(braking);
  updateBlinkers(blinkDir);

  // 6. Exibição periódica de Debug via Serial
  static unsigned long lastDebug = 0;
  if (millis() - lastDebug >= DEBUG_INTERVAL_MS) {
    lastDebug = millis();

    Serial.print(F("DIR:"));
    if (steerPct >= 0) Serial.print(F("+"));
    Serial.print(steerPct);   Serial.print(F("%"));

    Serial.print(F(" THR:"));
    if (throPct >= 0) Serial.print(F("+"));
    Serial.print(throPct);    Serial.print(F("%"));

    Serial.print(F(" HL:"));
    Serial.print(hlPct);      Serial.print(F("%"));

    Serial.print(F(" | F:"));
    switch (g_hlMode) {
      case HL_OFF:  Serial.print(F("OFF")); break;
      case HL_DIM:  Serial.print(F("40%")); break;
      case HL_FULL: Serial.print(F("100")); break;
    }

    Serial.print(F(" B:"));
    Serial.print(braking ? F("ON") : F("--"));

    Serial.print(F(" L:"));
    int tailPct = (g_tailCurrent * 100) / 255;
    Serial.print(tailPct);  Serial.print(F("%"));

    Serial.print(F(" P:"));
    switch (blinkDir) {
      case BLINK_LEFT:  Serial.println(F("<<E")); break;
      case BLINK_RIGHT: Serial.println(F("D>>")); break;
      default:          Serial.println(F("---")); break;
    }
  }
}

// ============================================================
// CONVERSÃO PARA PERCENTUAL
// ============================================================
int steeringToPercent(int ppm) {
  int deviation = ppm - g_steerCenter;
  if (deviation >= 0) {
    if (g_cal.steerDeflRight <= 0) return 0;
    return constrain((int)((long)deviation * 100 / g_cal.steerDeflRight), 0, 100);
  } else {
    if (g_cal.steerDeflLeft <= 0) return 0;
    return constrain((int)((long)deviation * 100 / g_cal.steerDeflLeft), -100, 0);
  }
}

int throttleToPercent(int ppm) {
  int deviation = ppm - g_throCenter;
  if (deviation >= 0) {
    if (g_cal.throDeflFwd <= 0) return 0;
    return constrain((int)((long)deviation * 100 / g_cal.throDeflFwd), 0, 100);
  } else {
    if (g_cal.throDeflBack <= 0) return 0;
    return constrain((int)((long)deviation * 100 / g_cal.throDeflBack), -100, 0);
  }
}

int headlightToPercent(int ppm) {
  int range = g_cal.headlightMax - g_cal.headlightMin;
  if (range <= 0) return 0;
  return constrain((int)((long)(ppm - g_cal.headlightMin) * 100 / range), 0, 100);
}

// ============================================================
// FUNÇÕES AUXILIARES - LEDs
// ============================================================
void allLEDsOff() {
  analogWrite(PIN_OUT_HEADLIGHT, 0);
  analogWrite(PIN_OUT_TAIL, 0);
  analogWrite(PIN_OUT_BRAKE, 0);
  digitalWrite(PIN_OUT_BLINK_L, LOW);
  digitalWrite(PIN_OUT_BLINK_R, LOW);
  g_tailCurrent = 0;
  g_tailTarget  = 0;
}

void blinkAllLEDs(int count, int intervalMs) {
  for (int i = 0; i < count; i++) {
    digitalWrite(PIN_OUT_BLINK_L, HIGH);
    digitalWrite(PIN_OUT_BLINK_R, HIGH);
    analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_100);
    analogWrite(PIN_OUT_TAIL, BRIGHTNESS_100);
    analogWrite(PIN_OUT_BRAKE, BRIGHTNESS_100);
    delay(intervalMs);
    allLEDsOff();
    delay(intervalMs);
  }
}

// ============================================================
// LEITURA NÃO-BLOQUEANTE + FILTRO
// ============================================================
int getFilteredSteering() {
  int raw;
  bool isNew = false;
  noInterrupts();
  raw = g_steerPulse;
  if (g_steerNewPulse) {
    isNew = true;
    g_steerNewPulse = false;
  }
  interrupts();

  if (isNew) {
    return g_steerFilter.update(raw);
  }
  return g_steerFilter.average();
}

int getFilteredThrottle() {
  int raw;
  bool isNew = false;
  noInterrupts();
  raw = g_throPulse;
  if (g_throNewPulse) {
    isNew = true;
    g_throNewPulse = false;
  }
  interrupts();

  if (isNew) {
    return g_throFilter.update(raw);
  }
  return g_throFilter.average();
}

int getFilteredHeadlight() {
  int raw;
  bool isNew = false;
  noInterrupts();
  raw = g_hlPulse;
  if (g_hlNewPulse) {
    isNew = true;
    g_hlNewPulse = false;
  }
  interrupts();

  if (isNew) {
    return g_hlFilter.update(raw);
  }
  return g_hlFilter.average();
}

// ============================================================
// LÓGICA DE CONTROLE
// ============================================================
HeadlightMode calcHeadlightMode(int hlPercent) {
  if (hlPercent < HEADLIGHT_THRESH_LOW)  return HL_OFF;
  if (hlPercent < HEADLIGHT_THRESH_HIGH) return HL_DIM;
  return HL_FULL;
}

bool isBraking(int throPct) {
  return (throPct < -THROTTLE_BRAKE_PERCENT);
}

BlinkDirection getBlinkDirection(int steerPct) {
  // Inversão física compensada no software:
  // steerPct > 70% (curva direita/alto) aciona o pisca esquerdo (pino 10)
  // steerPct < -70% (curva esquerda/baixo) aciona o pisca direito (pino 11)
  if (steerPct > STEERING_BLINK_PERCENT)  return BLINK_LEFT;
  if (steerPct < -STEERING_BLINK_PERCENT) return BLINK_RIGHT;
  return BLINK_NONE;
}

// ============================================================
// ATUALIZAÇÃO DAS SAÍDAS
// ============================================================
void updateHeadlight(HeadlightMode mode) {
  switch (mode) {
    case HL_OFF:  analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_OFF);  break;
    case HL_DIM:  analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_40);   break;
    case HL_FULL: analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_100);  break;
  }
}

void setTailLightTarget(HeadlightMode hlMode, bool braking) {
  if (braking) {
    g_tailTarget = BRIGHTNESS_100;
  } else if (hlMode != HL_OFF) {
    g_tailTarget = BRIGHTNESS_40;
  } else {
    g_tailTarget = BRIGHTNESS_OFF;
  }
}

void updateTailLightFade() {
  if (g_tailCurrent == g_tailTarget) return;

  unsigned long now = millis();
  if (now - g_lastFadeUpdate < FADE_STEP_INTERVAL_MS) return;
  g_lastFadeUpdate = now;

  if (g_tailCurrent < g_tailTarget) {
    g_tailCurrent += FADE_STEP_SIZE;
    if (g_tailCurrent > g_tailTarget) g_tailCurrent = g_tailTarget;
  } else {
    g_tailCurrent -= FADE_STEP_SIZE;
    if (g_tailCurrent < g_tailTarget) g_tailCurrent = g_tailTarget;
  }

  analogWrite(PIN_OUT_TAIL, g_tailCurrent);
}

void updateBrakeLight(bool braking) {
  digitalWrite(PIN_OUT_BRAKE, braking ? HIGH : LOW);
}

void updateBlinkers(BlinkDirection direction) {
  unsigned long now = millis();

  if (direction == BLINK_NONE) {
    digitalWrite(PIN_OUT_BLINK_L, LOW);
    digitalWrite(PIN_OUT_BLINK_R, LOW);
    g_blinkState = false;
    g_lastBlinkToggle = now;
    return;
  }

  if (now - g_lastBlinkToggle >= BLINK_INTERVAL_MS) {
    g_blinkState = !g_blinkState;
    g_lastBlinkToggle = now;
  }

  if (direction == BLINK_LEFT) {
    digitalWrite(PIN_OUT_BLINK_L, g_blinkState ? HIGH : LOW);
    digitalWrite(PIN_OUT_BLINK_R, LOW);
  } else {
    digitalWrite(PIN_OUT_BLINK_L, LOW);
    digitalWrite(PIN_OUT_BLINK_R, g_blinkState ? HIGH : LOW);
  }
}

// ============================================================
// EEPROM
// ============================================================
bool loadCalibration() {
  EEPROM.get(EEPROM_START_ADDR, g_cal);
  return (g_cal.magic == EEPROM_MAGIC_VALUE);
}

void saveCalibration() {
  g_cal.magic = EEPROM_MAGIC_VALUE;
  EEPROM.put(EEPROM_START_ADDR, g_cal);
}

void resetEEPROM() {
  g_cal.magic = 0x00;
  EEPROM.put(EEPROM_START_ADDR, g_cal);
}

void printCalibration() {
  Serial.println(F("\n┌─── Calibração (EEPROM) ───────────┐"));
  Serial.print(F("│ Volante:  esq=")); Serial.print(g_cal.steerDeflLeft);
  Serial.print(F("us  dir=")); Serial.print(g_cal.steerDeflRight); Serial.println(F("us"));
  Serial.print(F("│ Throttle: trás=")); Serial.print(g_cal.throDeflBack);
  Serial.print(F("us frente=")); Serial.print(g_cal.throDeflFwd); Serial.println(F("us"));
  Serial.print(F("│ Farol:    min=")); Serial.print(g_cal.headlightMin);
  Serial.print(F("us  max=")); Serial.print(g_cal.headlightMax); Serial.println(F("us"));

  Serial.println(F("├─── Centro Detectado (boot) ───────┤"));
  Serial.print(F("│ Volante:  ")); Serial.print(g_steerCenter); Serial.println(F("us"));
  Serial.print(F("│ Throttle: ")); Serial.print(g_throCenter);  Serial.println(F("us"));

  Serial.println(F("├─── Limiares (%) ──────────────────┤"));
  Serial.print(F("│ Pisca:      >")); Serial.print(STEERING_BLINK_PERCENT); Serial.println(F("%"));
  Serial.print(F("│ Freio:      <-")); Serial.print(THROTTLE_BRAKE_PERCENT); Serial.println(F("%"));
  Serial.print(F("│ Farol dim:  ")); Serial.print(HEADLIGHT_THRESH_LOW); Serial.println(F("%"));
  Serial.print(F("│ Farol full: ")); Serial.print(HEADLIGHT_THRESH_HIGH); Serial.println(F("%"));
  Serial.println(F("└──────────────────────────────────┘\n"));
}

// ============================================================
// AUTO-CENTRO (baseado em interrupções)
// ============================================================
void autoCenter() {
  Serial.println(F("\n⏱ Auto-centro: sticks CENTRALIZADOS (2 seg)..."));

  digitalWrite(PIN_OUT_BLINK_L, HIGH);
  digitalWrite(PIN_OUT_BLINK_R, HIGH);

  long steerSum = 0, throSum = 0;
  int  samples  = 0;
  unsigned long startTime = millis();

  // Limpa quaisquer flags pendentes
  noInterrupts();
  g_steerNewPulse = false;
  g_throNewPulse = false;
  interrupts();

  while (millis() - startTime < AUTOCENTER_DURATION_MS) {
    bool gotSteer = false;
    bool gotThro = false;
    int sVal = 0, tVal = 0;

    noInterrupts();
    if (g_steerNewPulse) {
      sVal = g_steerPulse;
      g_steerNewPulse = false;
      gotSteer = true;
    }
    if (g_throNewPulse) {
      tVal = g_throPulse;
      g_throNewPulse = false;
      gotThro = true;
    }
    interrupts();

    if (gotSteer && gotThro) {
      steerSum += sVal;
      throSum  += tVal;
      samples++;
    }
    delay(5);
  }

  digitalWrite(PIN_OUT_BLINK_L, LOW);
  digitalWrite(PIN_OUT_BLINK_R, LOW);

  if (samples > 0) {
    g_steerCenter = (int)(steerSum / samples);
    g_throCenter  = (int)(throSum  / samples);
    Serial.print(F("  ✓ Volante:  ")); Serial.print(g_steerCenter); Serial.println(F("us"));
    Serial.print(F("  ✓ Throttle: ")); Serial.print(g_throCenter);  Serial.println(F("us"));
  } else {
    g_steerCenter = DEFAULT_CENTER;
    g_throCenter  = DEFAULT_CENTER;
    Serial.println(F("  ⚠ Sem sinal! Usando 1500us."));
  }
  Serial.print(F("  (")); Serial.print(samples); Serial.println(F(" amostras)"));
}

// ============================================================
// CALIBRAÇÃO COMPLETA (baseada em interrupções)
// ============================================================
void runFullCalibration() {
  Serial.println(F("\n╔══════════════════════════════════════╗"));
  Serial.println(F("║    CALIBRAÇÃO COMPLETA  v5.1        ║"));
  Serial.println(F("║  Configure limitadores de curva     ║"));
  Serial.println(F("║  ANTES de calibrar!                 ║"));
  Serial.println(F("╚══════════════════════════════════════╝"));

  autoCenter();
  blinkAllLEDs(2, 150);
  delay(300);

  // ── PASSO 1: EXTREMOS ───────────────────────────────────
  Serial.println(F("\n[PASSO 1/2] EXTREMOS"));
  Serial.println(F("  Mova VOLANTE e ACELERADOR aos extremos (5s)...\n"));

  int sMin = g_steerCenter, sMax = g_steerCenter;
  int tMin = g_throCenter,  tMax = g_throCenter;

  unsigned long startTime = millis();
  bool ledTog = false;
  unsigned long lastLed = 0;

  noInterrupts();
  g_steerNewPulse = false;
  g_throNewPulse = false;
  interrupts();

  while (millis() - startTime < CAL_EXTREMES_DURATION_MS) {
    int s = -1;
    int t = -1;

    noInterrupts();
    if (g_steerNewPulse) {
      s = g_steerPulse;
      g_steerNewPulse = false;
    }
    if (g_throNewPulse) {
      t = g_throPulse;
      g_throNewPulse = false;
    }
    interrupts();

    if (s > 0) { if (s < sMin) sMin = s; if (s > sMax) sMax = s; }
    if (t > 0) { if (t < tMin) tMin = t; if (t > tMax) tMax = t; }

    if (millis() - lastLed >= 250) {
      ledTog = !ledTog;
      digitalWrite(PIN_OUT_BLINK_L, ledTog ? HIGH : LOW);
      digitalWrite(PIN_OUT_BLINK_R, ledTog ? LOW  : HIGH);
      lastLed = millis();
    }
    delay(5);
  }
  allLEDsOff();

  g_cal.steerDeflLeft  = g_steerCenter - sMin;
  g_cal.steerDeflRight = sMax - g_steerCenter;
  g_cal.throDeflBack   = g_throCenter  - tMin;
  g_cal.throDeflFwd    = tMax - g_throCenter;

  if (g_cal.steerDeflLeft + g_cal.steerDeflRight < CAL_MIN_RANGE)
    Serial.println(F("  ⚠ Faixa do volante pequena!"));
  if (g_cal.throDeflBack + g_cal.throDeflFwd < CAL_MIN_RANGE)
    Serial.println(F("  ⚠ Faixa do throttle pequena!"));

  Serial.print(F("  Volante:  ")); Serial.print(sMin);
  Serial.print(F(" ← [")); Serial.print(g_steerCenter);
  Serial.print(F("] → ")); Serial.println(sMax);
  Serial.print(F("  Throttle: ")); Serial.print(tMin);
  Serial.print(F(" ← [")); Serial.print(g_throCenter);
  Serial.print(F("] → ")); Serial.println(tMax);
  Serial.println(F("  ✓ Extremos registrados!"));

  blinkAllLEDs(2, 150);
  delay(300);

  // ── PASSO 2: FAROL ─────────────────────────────────────
  Serial.println(F("\n[PASSO 2/2] FAROL"));
  Serial.println(F("  Alterne a chave pelas 3 posições (5s)...\n"));

  analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_40);

  g_cal.headlightMin = PPM_VALID_MAX;
  g_cal.headlightMax = PPM_VALID_MIN;

  noInterrupts();
  g_hlNewPulse = false;
  interrupts();

  startTime = millis();
  while (millis() - startTime < CAL_HEADLIGHT_DURATION_MS) {
    int h = -1;

    noInterrupts();
    if (g_hlNewPulse) {
      h = g_hlPulse;
      g_hlNewPulse = false;
    }
    interrupts();

    if (h > 0) {
      if (h < g_cal.headlightMin) g_cal.headlightMin = h;
      if (h > g_cal.headlightMax) g_cal.headlightMax = h;
    }
    int bright = (millis() / 4) % 255;
    if (bright > 127) bright = 255 - bright;
    analogWrite(PIN_OUT_HEADLIGHT, bright);
    delay(5);
  }
  allLEDsOff();

  if (g_cal.headlightMax - g_cal.headlightMin < CAL_MIN_RANGE)
    Serial.println(F("  ⚠ Faixa do farol pequena!"));

  Serial.print(F("  Farol: ")); Serial.print(g_cal.headlightMin);
  Serial.print(F(" → ")); Serial.println(g_cal.headlightMax);
  Serial.println(F("  ✓ Farol registrado!"));

  saveCalibration();

  Serial.println(F("\n╔══════════════════════════════════════╗"));
  Serial.println(F("║      CALIBRAÇÃO CONCLUÍDA! ✓        ║"));
  Serial.println(F("╚══════════════════════════════════════╝"));
  printCalibration();
  blinkAllLEDs(5, 100);

  Serial.println(F("Pronto! Boa pilotagem.\n"));
}

// ============================================================
// COMANDOS SERIAL
// ============================================================
void processSerialCommand() {
  if (!Serial.available()) return;
  char cmd = Serial.read();
  while (Serial.available()) Serial.read();

  switch (cmd) {
    case 'C': case 'c':
      Serial.println(F("\n→ Iniciando calibração completa..."));
      runFullCalibration();
      break;

    case 'A': case 'a':
      Serial.println(F("\n→ Re-centralizando os sticks..."));
      autoCenter();
      Serial.println(F("  ✓ Centro atualizado!"));
      printCalibration();
      break;

    case 'P': case 'p':
      printCalibration();
      break;

    case 'R': case 'r':
      Serial.println(F("\n→ Resetando EEPROM..."));
      resetEEPROM();
      Serial.println(F("  Reinicie a placa ou envie o comando 'C'."));
      break;

    case '?': case 'h': case 'H':
      Serial.println(F("\n--- Comandos Serial ---"));
      Serial.println(F("  C = Calibração completa"));
      Serial.println(F("  A = Auto-centro (trim)"));
      Serial.println(F("  P = Imprimir calibração"));
      Serial.println(F("  R = Resetar EEPROM"));
      Serial.println(F("  ? = Ajuda\n"));
      break;
  }
}
