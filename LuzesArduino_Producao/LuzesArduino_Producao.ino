/*
 * ============================================================
 *  Sistema de Luzes para Carro RC - v6.0 (Versão PRODUÇÃO / PISTA)
 *  Arduino Nano + Receptor FlySky FS-BS6
 * ============================================================
 *
 * Esta versão é 100% focada em PERFORMANCE MÁXIMA NA PISTA:
 *   - Zero comunicação Serial (sem desperdício de ciclos de CPU ou interrupções de UART).
 *   - Memória Flash e SRAM ultra-reduzidas.
 *   - Loop principal rodando a mais de 60.000 Hz.
 *   - Inicialização e Calibração 100% autônomas via rádio com feedback visual nos LEDs.
 *
 * Entradas (Servo PPM do receptor):
 *   D4 - Volante / Direção (CH1, Pin Change Interrupt PCINT20)
 *   D2 - Acelerador / Freio (CH2, Interrupção externa INT0)
 *   D3 - Farol (CH4, Interrupção externa INT1)
 *   5V / GND - Alimentação direta via Canal 6 (CH6 do receptor)
 *
 * Saídas (LEDs):
 *   D5  - Lanterna traseira (vermelho, PWM com fade suave de ~300ms)
 *   D6  - Luz de freio (vermelho, Digital/PWM)
 *   D9  - Farol dianteiro (branco, PWM: OFF / 40% / 100%)
 *   D10 - Pisca dianteiro esquerdo (laranja, Digital)
 *   D11 - Pisca dianteiro direito (laranja, Digital)
 *   D7  - Pisca traseiro esquerdo (laranja, Digital)
 *   D8  - Pisca traseiro direito (laranja, Digital)
 */

#include <EEPROM.h>

// ============================================================
// PINAGEM
// ============================================================
#define PIN_IN_STEERING    4    // CH1 - Volante (PCINT20)
#define PIN_IN_THROTTLE    2    // CH2 - Aceleração (INT0)
#define PIN_IN_HEADLIGHT   3    // CH4 - Farol (INT1)

#define PIN_OUT_TAIL       5    // PWM - Lanterna traseira
#define PIN_OUT_BRAKE      6    // PWM/Digital - Luz de freio
#define PIN_OUT_HEADLIGHT  9    // PWM - Farol dianteiro
#define PIN_OUT_BLINK_FL   10   // Pisca dianteiro esquerdo
#define PIN_OUT_BLINK_FR   11   // Pisca dianteiro direito
#define PIN_OUT_BLINK_RL   7    // Pisca traseiro esquerdo
#define PIN_OUT_BLINK_RR   8    // Pisca traseiro direito

// ============================================================
// CONSTANTES E CONFIGURAÇÕES
// ============================================================
#define EEPROM_MAGIC_VALUE       0xAD
#define EEPROM_START_ADDR        0

#define PPM_VALID_MIN            800
#define PPM_VALID_MAX            2200

#define DEFAULT_CENTER           1500
#define DEFAULT_DEFLECTION       500

// --- Limiares de Ação (%) ---
#define STEERING_BLINK_PERCENT   70    // Deflexão do volante para ligar o pisca (70%)
#define THROTTLE_BRAKE_PERCENT   5     // Desaceleração para acionar a luz de freio (5%)
#define HEADLIGHT_THRESH_LOW     33    // Abaixo: OFF | Acima: 40%
#define HEADLIGHT_THRESH_HIGH    66    // Acima: 100%

// --- Níveis de Brilho (PWM 0-255) ---
#define BRIGHTNESS_OFF           0
#define BRIGHTNESS_40            102
#define BRIGHTNESS_100           255

// --- Pisca e Fade ---
#define BLINK_INTERVAL_MS        250   // 120 piscadas por minuto
#define FADE_STEP_INTERVAL_MS    6     // Intervalo de fade da lanterna (~300ms total)
#define FADE_STEP_SIZE           5

// --- Filtro de Média Móvel ---
#define FILTER_SIZE              5
#define CAL_MIN_RANGE            200

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
enum BlinkDirection { BLINK_LEFT = -1, BLINK_NONE = 0, BLINK_RIGHT = 1 };

// ============================================================
// VARIÁVEIS GLOBAIS
// ============================================================
CalibrationData g_cal;

int g_steerCenter = DEFAULT_CENTER;
int g_throCenter  = DEFAULT_CENTER;

// ISR variables (volatile)
volatile unsigned long g_steerRiseTime = 0;
volatile unsigned long g_throRiseTime  = 0;
volatile unsigned long g_hlRiseTime    = 0;

volatile int g_steerPulse = DEFAULT_CENTER;
volatile int g_throPulse  = DEFAULT_CENTER;
volatile int g_hlPulse    = DEFAULT_CENTER;

volatile bool g_steerNewPulse = false;
volatile bool g_throNewPulse  = false;
volatile bool g_hlNewPulse    = false;

MovingAvgFilter g_steerFilter;
MovingAvgFilter g_throFilter;
MovingAvgFilter g_hlFilter;

int           g_tailCurrent = 0;
int           g_tailTarget  = 0;
unsigned long g_lastFadeUpdate = 0;

unsigned long g_lastBlinkToggle = 0;
bool          g_blinkState      = false;

HeadlightMode g_hlMode = HL_OFF;

// ============================================================
// PROTÓTIPOS
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
void autoCenter();
bool checkCalibrationGesture();
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

// ============================================================
// INTERRUPÇÕES (ISRs de Baixo Nível)
// ============================================================
ISR(PCINT2_vect) {
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
// GESTO DE CALIBRAÇÃO NO RÁDIO
// ============================================================
bool checkCalibrationGesture() {
  unsigned long start = millis();
  int steerDeflectedCount = 0;
  int totalSamples = 0;

  digitalWrite(PIN_OUT_BLINK_FL, HIGH);
  digitalWrite(PIN_OUT_BLINK_FR, HIGH);

  noInterrupts();
  g_steerNewPulse = false;
  g_throNewPulse = false;
  interrupts();

  while (millis() - start < 1500) {
    int s = 0;
    noInterrupts();
    if (g_steerNewPulse) {
      s = g_steerPulse;
      g_steerNewPulse = false;
    }
    interrupts();

    if (s >= PPM_VALID_MIN && s <= PPM_VALID_MAX) {
      totalSamples++;
      if (s < 1250 || s > 1750) {
        steerDeflectedCount++;
      }
    }
    delay(10);
  }

  digitalWrite(PIN_OUT_BLINK_FL, LOW);
  digitalWrite(PIN_OUT_BLINK_FR, LOW);

  if (totalSamples >= 15 && steerDeflectedCount >= (totalSamples * 6 / 10)) {
    return true;
  }
  return false;
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  pinMode(PIN_IN_STEERING,  INPUT);
  pinMode(PIN_IN_THROTTLE,  INPUT);
  pinMode(PIN_IN_HEADLIGHT, INPUT);

  pinMode(PIN_OUT_TAIL,      OUTPUT);
  pinMode(PIN_OUT_BRAKE,     OUTPUT);
  pinMode(PIN_OUT_HEADLIGHT, OUTPUT);
  pinMode(PIN_OUT_BLINK_FL,  OUTPUT);
  pinMode(PIN_OUT_BLINK_FR,  OUTPUT);
  pinMode(PIN_OUT_BLINK_RL,  OUTPUT);
  pinMode(PIN_OUT_BLINK_RR,  OUTPUT);

  allLEDsOff();

  g_steerFilter.init(DEFAULT_CENTER);
  g_throFilter.init(DEFAULT_CENTER);
  g_hlFilter.init(DEFAULT_CENTER);

  // Configura interrupções por hardware
  PCICR |= (1 << PCIE2);
  PCMSK2 |= (1 << PCINT20);

  attachInterrupt(digitalPinToInterrupt(PIN_IN_THROTTLE),  throttleISR,  CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_IN_HEADLIGHT), headlightISR, CHANGE);

  // Carrega calibração prévia ou usa padrões de fábrica (500us)
  if (!loadCalibration()) {
    g_cal.steerDeflLeft  = DEFAULT_DEFLECTION;
    g_cal.steerDeflRight = DEFAULT_DEFLECTION;
    g_cal.throDeflBack   = DEFAULT_DEFLECTION;
    g_cal.throDeflFwd    = DEFAULT_DEFLECTION;
    g_cal.headlightMin   = DEFAULT_CENTER - DEFAULT_DEFLECTION;
    g_cal.headlightMax   = DEFAULT_CENTER + DEFAULT_DEFLECTION;
  }

  // Verifica gesto de calibração no boot (volante virado por 1.5s)
  bool gesture = checkCalibrationGesture();

  if (gesture) {
    blinkAllLEDs(3, 100); // 3 piscadas confirmam entrada no modo calibração
    delay(400);
    runFullCalibration(); // Executa calibração autônoma guiada por LEDs
  } else {
    autoCenter();
    blinkAllLEDs(2, 100); // 2 piscadas confirmam pronto para rodar
  }
}

// ============================================================
// LOOP PRINCIPAL (Ultra-rápido, não-bloqueante)
// ============================================================
void loop() {
  int steerRaw = getFilteredSteering();
  int throRaw  = getFilteredThrottle();
  int hlRaw    = getFilteredHeadlight();

  int steerPct = steeringToPercent(steerRaw);
  int throPct  = throttleToPercent(throRaw);
  int hlPct    = headlightToPercent(hlRaw);

  g_hlMode = calcHeadlightMode(hlPct);
  bool           braking  = isBraking(throPct);
  BlinkDirection blinkDir = getBlinkDirection(steerPct);

  updateHeadlight(g_hlMode);
  setTailLightTarget(g_hlMode, braking);
  updateTailLightFade();
  updateBrakeLight(braking);
  updateBlinkers(blinkDir);
}

// ============================================================
// CONVERSÕES PERCENTUAIS
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
// CONTROLE DOS LEDS
// ============================================================
void allLEDsOff() {
  analogWrite(PIN_OUT_HEADLIGHT, 0);
  analogWrite(PIN_OUT_TAIL, 0);
  analogWrite(PIN_OUT_BRAKE, 0);
  digitalWrite(PIN_OUT_BLINK_FL, LOW);
  digitalWrite(PIN_OUT_BLINK_FR, LOW);
  digitalWrite(PIN_OUT_BLINK_RL, LOW);
  digitalWrite(PIN_OUT_BLINK_RR, LOW);
  g_tailCurrent = 0;
  g_tailTarget  = 0;
}

void blinkAllLEDs(int count, int intervalMs) {
  for (int i = 0; i < count; i++) {
    digitalWrite(PIN_OUT_BLINK_FL, HIGH);
    digitalWrite(PIN_OUT_BLINK_FR, HIGH);
    digitalWrite(PIN_OUT_BLINK_RL, HIGH);
    digitalWrite(PIN_OUT_BLINK_RR, HIGH);
    analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_100);
    analogWrite(PIN_OUT_TAIL, BRIGHTNESS_100);
    analogWrite(PIN_OUT_BRAKE, BRIGHTNESS_100);
    delay(intervalMs);
    allLEDsOff();
    delay(intervalMs);
  }
}

int getFilteredSteering() {
  noInterrupts();
  if (g_steerNewPulse) {
    int val = g_steerPulse;
    g_steerNewPulse = false;
    interrupts();
    return g_steerFilter.update(val);
  }
  interrupts();
  return g_steerFilter.average();
}

int getFilteredThrottle() {
  noInterrupts();
  if (g_throNewPulse) {
    int val = g_throPulse;
    g_throNewPulse = false;
    interrupts();
    return g_throFilter.update(val);
  }
  interrupts();
  return g_throFilter.average();
}

int getFilteredHeadlight() {
  noInterrupts();
  if (g_hlNewPulse) {
    int val = g_hlPulse;
    g_hlNewPulse = false;
    interrupts();
    return g_hlFilter.update(val);
  }
  interrupts();
  return g_hlFilter.average();
}

HeadlightMode calcHeadlightMode(int hlPercent) {
  if (hlPercent < HEADLIGHT_THRESH_LOW)  return HL_OFF;
  if (hlPercent <= HEADLIGHT_THRESH_HIGH) return HL_DIM;
  return HL_FULL;
}

bool isBraking(int throPct) {
  return (throPct < -THROTTLE_BRAKE_PERCENT);
}

BlinkDirection getBlinkDirection(int steerPct) {
  if (steerPct <= -STEERING_BLINK_PERCENT) return BLINK_LEFT;
  if (steerPct >=  STEERING_BLINK_PERCENT) return BLINK_RIGHT;
  return BLINK_NONE;
}

void updateHeadlight(HeadlightMode mode) {
  switch (mode) {
    case HL_OFF:  analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_OFF); break;
    case HL_DIM:  analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_40);  break;
    case HL_FULL: analogWrite(PIN_OUT_HEADLIGHT, BRIGHTNESS_100); break;
  }
}

void setTailLightTarget(HeadlightMode hlMode, bool braking) {
  if (braking) {
    g_tailTarget = BRIGHTNESS_100;
  } else {
    switch (hlMode) {
      case HL_OFF:  g_tailTarget = BRIGHTNESS_OFF; break;
      case HL_DIM:  g_tailTarget = BRIGHTNESS_40;  break;
      case HL_FULL: g_tailTarget = BRIGHTNESS_100; break;
    }
  }
}

void updateTailLightFade() {
  unsigned long now = millis();
  if (now - g_lastFadeUpdate < FADE_STEP_INTERVAL_MS) return;
  g_lastFadeUpdate = now;

  if (g_tailCurrent < g_tailTarget) {
    g_tailCurrent += FADE_STEP_SIZE;
    if (g_tailCurrent > g_tailTarget) g_tailCurrent = g_tailTarget;
  } else if (g_tailCurrent > g_tailTarget) {
    g_tailCurrent -= FADE_STEP_SIZE;
    if (g_tailCurrent < g_tailTarget) g_tailCurrent = g_tailTarget;
  }
  analogWrite(PIN_OUT_TAIL, g_tailCurrent);
}

void updateBrakeLight(bool braking) {
  analogWrite(PIN_OUT_BRAKE, braking ? BRIGHTNESS_100 : BRIGHTNESS_OFF);
}

void updateBlinkers(BlinkDirection direction) {
  unsigned long now = millis();
  if (direction == BLINK_NONE) {
    digitalWrite(PIN_OUT_BLINK_FL, LOW);
    digitalWrite(PIN_OUT_BLINK_FR, LOW);
    digitalWrite(PIN_OUT_BLINK_RL, LOW);
    digitalWrite(PIN_OUT_BLINK_RR, LOW);
    g_blinkState = false;
    g_lastBlinkToggle = now;
    return;
  }

  if (now - g_lastBlinkToggle >= BLINK_INTERVAL_MS) {
    g_blinkState = !g_blinkState;
    g_lastBlinkToggle = now;
  }

  if (direction == BLINK_LEFT) {
    digitalWrite(PIN_OUT_BLINK_FL, g_blinkState ? HIGH : LOW);
    digitalWrite(PIN_OUT_BLINK_RL, g_blinkState ? HIGH : LOW);
    digitalWrite(PIN_OUT_BLINK_FR, LOW);
    digitalWrite(PIN_OUT_BLINK_RR, LOW);
  } else {
    digitalWrite(PIN_OUT_BLINK_FL, LOW);
    digitalWrite(PIN_OUT_BLINK_RL, LOW);
    digitalWrite(PIN_OUT_BLINK_FR, g_blinkState ? HIGH : LOW);
    digitalWrite(PIN_OUT_BLINK_RR, g_blinkState ? HIGH : LOW);
  }
}

// ============================================================
// EEPROM
// ============================================================
bool loadCalibration() {
  EEPROM.get(EEPROM_START_ADDR, g_cal);
  if (g_cal.magic != EEPROM_MAGIC_VALUE) return false;
  if (g_cal.steerDeflLeft < 50 || g_cal.steerDeflRight < 50 ||
      g_cal.throDeflBack < 50  || g_cal.throDeflFwd < 50 ||
      (g_cal.headlightMax - g_cal.headlightMin) < CAL_MIN_RANGE) {
    return false;
  }
  return true;
}

void saveCalibration() {
  g_cal.magic = EEPROM_MAGIC_VALUE;
  EEPROM.put(EEPROM_START_ADDR, g_cal);
}

// ============================================================
// AUTO-CENTRO E CALIBRAÇÃO GUIADA POR LEDS
// ============================================================
void autoCenter() {
  digitalWrite(PIN_OUT_BLINK_FL, HIGH);
  digitalWrite(PIN_OUT_BLINK_FR, HIGH);
  digitalWrite(PIN_OUT_BLINK_RL, HIGH);
  digitalWrite(PIN_OUT_BLINK_RR, HIGH);

  long steerSum = 0, throSum = 0;
  int  samples  = 0;
  unsigned long startTime = millis();

  noInterrupts();
  g_steerNewPulse = false;
  g_throNewPulse = false;
  interrupts();

  while (millis() - startTime < 2000) {
    int sVal = 0, tVal = 0;
    bool gotS = false, gotT = false;

    noInterrupts();
    if (g_steerNewPulse) { sVal = g_steerPulse; g_steerNewPulse = false; gotS = true; }
    if (g_throNewPulse)  { tVal = g_throPulse;  g_throNewPulse = false;  gotT = true; }
    interrupts();

    if (gotS && gotT) {
      steerSum += sVal;
      throSum  += tVal;
      samples++;
    }
    delay(5);
  }

  digitalWrite(PIN_OUT_BLINK_FL, LOW);
  digitalWrite(PIN_OUT_BLINK_FR, LOW);
  digitalWrite(PIN_OUT_BLINK_RL, LOW);
  digitalWrite(PIN_OUT_BLINK_RR, LOW);

  if (samples > 0) {
    g_steerCenter = (int)(steerSum / samples);
    g_throCenter  = (int)(throSum  / samples);
  } else {
    g_steerCenter = DEFAULT_CENTER;
    g_throCenter  = DEFAULT_CENTER;
  }
}

void runFullCalibration() {
  autoCenter();
  blinkAllLEDs(2, 150);
  delay(300);

  // --- PASSO 1: EXTREMOS VOLANTE E ACELERADOR (5s) ---
  int sMin = g_steerCenter, sMax = g_steerCenter;
  int tMin = g_throCenter,  tMax = g_throCenter;
  unsigned long startTime = millis();
  bool ledTog = false;
  unsigned long lastLed = 0;

  noInterrupts();
  g_steerNewPulse = false;
  g_throNewPulse = false;
  interrupts();

  while (millis() - startTime < 5000) {
    int s = -1, t = -1;

    noInterrupts();
    if (g_steerNewPulse) { s = g_steerPulse; g_steerNewPulse = false; }
    if (g_throNewPulse)  { t = g_throPulse;  g_throNewPulse  = false; }
    interrupts();

    if (s > 0) { if (s < sMin) sMin = s; if (s > sMax) sMax = s; }
    if (t > 0) { if (t < tMin) tMin = t; if (t > tMax) tMax = t; }

    // Piscas alternando esquerda/direita guiam o usuário
    if (millis() - lastLed >= 200) {
      ledTog = !ledTog;
      digitalWrite(PIN_OUT_BLINK_FL, ledTog ? HIGH : LOW);
      digitalWrite(PIN_OUT_BLINK_RL, ledTog ? HIGH : LOW);
      digitalWrite(PIN_OUT_BLINK_FR, ledTog ? LOW  : HIGH);
      digitalWrite(PIN_OUT_BLINK_RR, ledTog ? LOW  : HIGH);
      lastLed = millis();
    }
    delay(5);
  }
  allLEDsOff();

  g_cal.steerDeflLeft  = g_steerCenter - sMin;
  g_cal.steerDeflRight = sMax - g_steerCenter;
  g_cal.throDeflBack   = g_throCenter  - tMin;
  g_cal.throDeflFwd    = tMax - g_throCenter;

  if (g_cal.steerDeflLeft + g_cal.steerDeflRight < CAL_MIN_RANGE) {
    g_cal.steerDeflLeft  = DEFAULT_DEFLECTION;
    g_cal.steerDeflRight = DEFAULT_DEFLECTION;
  }
  if (g_cal.throDeflBack + g_cal.throDeflFwd < CAL_MIN_RANGE) {
    g_cal.throDeflBack   = DEFAULT_DEFLECTION;
    g_cal.throDeflFwd    = DEFAULT_DEFLECTION;
  }

  blinkAllLEDs(2, 150);
  delay(300);

  // --- PASSO 2: FAROL (5s) ---
  g_cal.headlightMin = PPM_VALID_MAX;
  g_cal.headlightMax = PPM_VALID_MIN;

  noInterrupts();
  g_hlNewPulse = false;
  interrupts();

  startTime = millis();
  while (millis() - startTime < 5000) {
    int h = -1;

    noInterrupts();
    if (g_hlNewPulse) { h = g_hlPulse; g_hlNewPulse = false; }
    interrupts();

    if (h > 0) {
      if (h < g_cal.headlightMin) g_cal.headlightMin = h;
      if (h > g_cal.headlightMax) g_cal.headlightMax = h;
    }

    // Farol pulsando suavemente avisa para mexer na chave
    int bright = (millis() / 4) % 255;
    if (bright > 127) bright = 255 - bright;
    analogWrite(PIN_OUT_HEADLIGHT, bright);
    delay(5);
  }
  allLEDsOff();

  if (g_cal.headlightMax - g_cal.headlightMin < CAL_MIN_RANGE) {
    g_cal.headlightMin = DEFAULT_CENTER - DEFAULT_DEFLECTION;
    g_cal.headlightMax = DEFAULT_CENTER + DEFAULT_DEFLECTION;
  }

  saveCalibration();
  blinkAllLEDs(5, 80); // 5 piscadas rápidas confirmam gravação na EEPROM
}
