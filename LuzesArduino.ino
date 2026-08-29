/*
 * ============================================================
 *  Sistema de Luzes para Carro RC - v2.0
 *  Arduino Nano + Receptor FlySky FS-BS6
 * ============================================================
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
 *
 * Melhorias v2.0:
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
#define PIN_OUT_BLINK_FL   10   // Pisca dianteiro esquerdo
#define PIN_OUT_BLINK_FR   11   // Pisca dianteiro direito
#define PIN_OUT_BLINK_RL   7    // Pisca traseiro esquerdo
#define PIN_OUT_BLINK_RR   8    // Pisca traseiro direito

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
void processSerialCommand();
void runSimulationStep();

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

// --- Simulação / Modo de Teste ---
bool          g_testActive      = false;
bool          g_manualSim       = false;
unsigned long g_testStartTime   = 0;
int           g_simSteer        = DEFAULT_CENTER;
int           g_simThro         = DEFAULT_CENTER;
int           g_simHl           = DEFAULT_CENTER - DEFAULT_DEFLECTION; // 1000us (Farol OFF no boot)
uint8_t       g_manualHlStage   = 0; // 0 = OFF, 1 = 40%, 2 = 100%
unsigned long g_steerTimeout    = 0; // Timestamp de término da ação do volante
unsigned long g_throTimeout     = 0; // Timestamp de término da ação do acelerador

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
// VERIFICAÇÃO DE GESTO DE CALIBRAÇÃO NO RÁDIO
// ============================================================
// Ao ligar o carro, se o usuário mantiver o volante todo virado (para esq/dir)
// por 1.5s, o Arduino entra no modo de calibração sem precisar de computador.
bool checkCalibrationGesture() {
  unsigned long start = millis();
  int steerDeflectedCount = 0;
  int totalSamples = 0;

  // Acende piscas dianteiros para indicar a janela de verificação no boot
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
      // Considera defletido se o volante estiver virado > 60% para esquerda (< 1250us) ou direita (> 1750us)
      if (s < 1250 || s > 1750) {
        steerDeflectedCount++;
      }
    }
    delay(10);
  }

  digitalWrite(PIN_OUT_BLINK_FL, LOW);
  digitalWrite(PIN_OUT_BLINK_FR, LOW);

  // Considera gesto válido se houve sinal consistente e o volante permaneceu virado
  if (totalSamples >= 15 && steerDeflectedCount >= (totalSamples * 6 / 10)) {
    return true;
  }
  return false;
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
  pinMode(PIN_OUT_BLINK_FL,  OUTPUT);
  pinMode(PIN_OUT_BLINK_FR,  OUTPUT);
  pinMode(PIN_OUT_BLINK_RL,  OUTPUT);
  pinMode(PIN_OUT_BLINK_RR,  OUTPUT);

  allLEDsOff();

  // Inicializa filtros de média móvel
  g_steerFilter.init(DEFAULT_CENTER);
  g_throFilter.init(DEFAULT_CENTER);
  g_hlFilter.init(DEFAULT_CENTER - DEFAULT_DEFLECTION); // 1000us (Farol OFF no boot)

  // Inicializa a Serial (para bancada e debug)
  Serial.begin(SERIAL_BAUD);
  Serial.println(F("\n==================================="));
  Serial.println(F(" Sistema de Luzes RC - v2.0"));
  Serial.println(F(" 100% Interrupt-driven (Não-bloqueante)"));
  Serial.println(F("==================================="));
  Serial.println(F(" C=Calibrar A=Centro P=Print ?=Ajuda\n"));

  // Configura e habilita as interrupções de hardware
  // 1. Pin Change Interrupt no pino D4 (PCINT20)
  PCICR |= (1 << PCIE2);      // Habilita PCINT para Port D (D0-D7)
  PCMSK2 |= (1 << PCINT20);   // Habilita interrupção específica para o pino D4 (PCINT20)

  // 2. Interrupções externas nos pinos D2 (INT0) e D3 (INT1)
  attachInterrupt(digitalPinToInterrupt(PIN_IN_THROTTLE),  throttleISR,  CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_IN_HEADLIGHT), headlightISR, CHANGE);

  // 3. Carrega calibração prévia da EEPROM ou adota os padrões de fábrica universais (500us)
  if (loadCalibration()) {
    Serial.println(F("✓ Calibração carregada da EEPROM."));
  } else {
    Serial.println(F("⚠ Sem calibração válida na EEPROM. Aplicando padrões de fábrica (500us)."));
    g_cal.steerDeflLeft  = DEFAULT_DEFLECTION;
    g_cal.steerDeflRight = DEFAULT_DEFLECTION;
    g_cal.throDeflBack   = DEFAULT_DEFLECTION;
    g_cal.throDeflFwd    = DEFAULT_DEFLECTION;
    g_cal.headlightMin   = DEFAULT_CENTER - DEFAULT_DEFLECTION;
    g_cal.headlightMax   = DEFAULT_CENTER + DEFAULT_DEFLECTION;
  }

  // 4. Verifica se o usuário realizou o Gesto de Calibração (Segurar volante virado no boot)
  Serial.println(F("⏱ Verificando se há gesto de calibração no rádio (1.5 seg)..."));
  bool gestureTriggered = checkCalibrationGesture();

  if (gestureTriggered) {
    Serial.println(F("\n🎯 [GESTO NO RÁDIO DETECTADO!]"));
    Serial.println(F("→ Entrando no modo de calibração autônoma de campo!"));
    blinkAllLEDs(3, 100); // 3 piscadas confirmam entrada
    delay(400);
    runFullCalibration(); // Executa calibração completa guiada por LEDs e salva na EEPROM
  } else {
    // Inicialização normal rápida: auto-centro de neutro
    autoCenter();
    blinkAllLEDs(2, 100); // 2 piscadas confirmam pronto para rodar
  }

  printCalibration();
  Serial.println(F("Pronto! Boa pilotagem.\n"));
}

// ============================================================
// LOOP PRINCIPAL
// ============================================================
void loop() {
  // 1. Processa comandos enviados via Serial
  processSerialCommand();

  // 2. Lê valores (do simulador se ativo, senão do receptor)
  int steerRaw, throRaw, hlRaw;
  if (g_testActive) {
    runSimulationStep();
    steerRaw = g_simSteer;
    throRaw  = g_simThro;
    hlRaw    = g_simHl;
  } else if (g_manualSim) {
    // Gerenciamento de expiração dos comandos temporizados (+500ms por toque)
    if (g_steerTimeout > 0 && millis() >= g_steerTimeout) {
      g_simSteer = g_steerCenter;
      g_steerTimeout = 0;
    }
    if (g_throTimeout > 0 && millis() >= g_throTimeout) {
      g_simThro = g_throCenter;
      g_throTimeout = 0;
    }
    steerRaw = g_simSteer;
    throRaw  = g_simThro;
    hlRaw    = g_simHl;
  } else {
    steerRaw = getFilteredSteering();
    throRaw  = getFilteredThrottle();
    hlRaw    = getFilteredHeadlight();
  }

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

  // 6. Exibição periódica de Debug via Serial (imprime em mudanças de estado e durante ações)
  static unsigned long lastDebug = 0;
  static int lastSteer = 999, lastThro = 999, lastHl = 999;
  static bool lastBrake = false;
  static BlinkDirection lastBlink = BLINK_NONE;

  bool stateChanged = (steerPct != lastSteer || throPct != lastThro || hlPct != lastHl ||
                       braking != lastBrake || blinkDir != lastBlink);

  if (!g_testActive && (stateChanged || (millis() - lastDebug >= 1000 && (steerPct != 0 || throPct != 0 || braking || g_hlMode != HL_OFF)))) {
    lastDebug = millis();
    lastSteer = steerPct;
    lastThro  = throPct;
    lastHl    = hlPct;
    lastBrake = braking;
    lastBlink = blinkDir;

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
      case HL_FULL: Serial.print(F("100%")); break;
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

  digitalWrite(PIN_OUT_BLINK_FL, HIGH);
  digitalWrite(PIN_OUT_BLINK_FR, HIGH);
  digitalWrite(PIN_OUT_BLINK_RL, HIGH);
  digitalWrite(PIN_OUT_BLINK_RR, HIGH);

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

  digitalWrite(PIN_OUT_BLINK_FL, LOW);
  digitalWrite(PIN_OUT_BLINK_FR, LOW);
  digitalWrite(PIN_OUT_BLINK_RL, LOW);
  digitalWrite(PIN_OUT_BLINK_RR, LOW);

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
  Serial.println(F("║    CALIBRAÇÃO COMPLETA  v2.0        ║"));
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
    Serial.println(F("  ⚠ Faixa do volante pequena! Usando padrão (500us)."));
    g_cal.steerDeflLeft  = DEFAULT_DEFLECTION;
    g_cal.steerDeflRight = DEFAULT_DEFLECTION;
  }
  if (g_cal.throDeflBack + g_cal.throDeflFwd < CAL_MIN_RANGE) {
    Serial.println(F("  ⚠ Faixa do throttle pequena! Usando padrão (500us)."));
    g_cal.throDeflBack   = DEFAULT_DEFLECTION;
    g_cal.throDeflFwd    = DEFAULT_DEFLECTION;
  }

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

  if (g_cal.headlightMax - g_cal.headlightMin < CAL_MIN_RANGE) {
    Serial.println(F("  ⚠ Faixa do farol pequena! Usando padrão (1000us a 2000us)."));
    g_cal.headlightMin = DEFAULT_CENTER - DEFAULT_DEFLECTION;
    g_cal.headlightMax = DEFAULT_CENTER + DEFAULT_DEFLECTION;
  }

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
// ============================================================
// COMANDOS SERIAL
// ============================================================
void processSerialCommand() {
  while (Serial.available() > 0) {
    char cmd = Serial.read();
    // Ignora quebras de linha e espaços em branco
    if (cmd == '\r' || cmd == '\n' || cmd == ' ' || cmd == '\t') continue;

    switch (cmd) {
      case 'C': case 'c':
        Serial.println(F("\n→ Iniciando calibração completa..."));
        runFullCalibration();
        break;

      case 'Z': case 'z':
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

      case 'T': case 't':
        Serial.println(F("\n→ Iniciando simulação de circuito de 60 segundos..."));
        g_testActive = true;
        g_manualSim = false;
        g_testStartTime = millis();
        break;

      case 'W': case 'w': {
        g_manualSim = true;
        g_testActive = false;
        unsigned long now = millis();
        if (g_throTimeout > now && g_simThro > g_throCenter) {
          g_throTimeout += 500;
        } else {
          g_throTimeout = now + 500;
        }
        g_simThro = g_throCenter + g_cal.throDeflFwd;
        Serial.print(F("🎮 [MANUAL] Acelerar Frente (+100%) | Freio OFF | Duração: "));
        Serial.print(g_throTimeout - now);
        Serial.println(F("ms"));
        break;
      }

      case 'S': case 's': {
        g_manualSim = true;
        g_testActive = false;
        unsigned long now = millis();
        if (g_throTimeout > now && g_simThro < g_throCenter) {
          g_throTimeout += 500;
        } else {
          g_throTimeout = now + 500;
        }
        g_simThro = g_throCenter - g_cal.throDeflBack;
        Serial.print(F("🎮 [MANUAL] Freiar / Ré (-100%) | Freio ON | Duração: "));
        Serial.print(g_throTimeout - now);
        Serial.println(F("ms"));
        break;
      }

      case 'A': case 'a': {
        g_manualSim = true;
        g_testActive = false;
        unsigned long now = millis();
        if (g_steerTimeout > now && g_simSteer < g_steerCenter) {
          g_steerTimeout += 500;
        } else {
          g_steerTimeout = now + 500;
        }
        g_simSteer = g_steerCenter - g_cal.steerDeflLeft;
        Serial.print(F("🎮 [MANUAL] Virar Esquerda (-100%) | Pisca Esq ON | Duração: "));
        Serial.print(g_steerTimeout - now);
        Serial.println(F("ms"));
        break;
      }

      case 'D': case 'd': {
        g_manualSim = true;
        g_testActive = false;
        unsigned long now = millis();
        if (g_steerTimeout > now && g_simSteer > g_steerCenter) {
          g_steerTimeout += 500;
        } else {
          g_steerTimeout = now + 500;
        }
        g_simSteer = g_steerCenter + g_cal.steerDeflRight;
        Serial.print(F("🎮 [MANUAL] Virar Direita (+100%) | Pisca Dir ON | Duração: "));
        Serial.print(g_steerTimeout - now);
        Serial.println(F("ms"));
        break;
      }

      case 'F': case 'f': {
        g_manualSim = true;
        g_testActive = false;
        if (g_manualHlStage < 2) g_manualHlStage++;
        if (g_manualHlStage == 1) {
          g_simHl = g_cal.headlightMin + (long)50 * (g_cal.headlightMax - g_cal.headlightMin) / 100;
          Serial.println(F("🎮 [MANUAL] Farol (+): PARCIAL (40% PWM)"));
        } else {
          g_simHl = g_cal.headlightMax;
          Serial.println(F("🎮 [MANUAL] Farol (+): TOTAL (100% PWM)"));
        }
        break;
      }

      case 'G': case 'g': {
        g_manualSim = true;
        g_testActive = false;
        if (g_manualHlStage > 0) g_manualHlStage--;
        if (g_manualHlStage == 1) {
          g_simHl = g_cal.headlightMin + (long)50 * (g_cal.headlightMax - g_cal.headlightMin) / 100;
          Serial.println(F("🎮 [MANUAL] Farol (-): PARCIAL (40% PWM)"));
        } else {
          g_simHl = g_cal.headlightMin;
          Serial.println(F("🎮 [MANUAL] Farol (-): APAGADO (OFF)"));
        }
        break;
      }

      case 'X': case 'x': {
        g_manualSim = true;
        g_testActive = false;
        g_steerTimeout = 0;
        g_throTimeout  = 0;
        g_simSteer = g_steerCenter;
        g_simThro  = g_throCenter;
        Serial.println(F("🎮 [MANUAL] Centralizado (Neutro) | Piscas & Freio OFF"));
        break;
      }

      case 'N': case 'n':
        g_manualSim = false;
        g_testActive = false;
        g_steerTimeout = 0;
        g_throTimeout  = 0;
        Serial.println(F("→ Retornando ao modo Rádio Receptor Normal."));
        break;

      case '?': case 'h': case 'H':
        Serial.println(F("\n--- Comandos de Teclado & Simulação ---"));
        Serial.println(F("  W = Acelerar (+500ms por toque)"));
        Serial.println(F("  S = Freiar / Ré (+500ms por toque)"));
        Serial.println(F("  A = Virar Esquerda (+500ms por toque)"));
        Serial.println(F("  D = Virar Direita (+500ms por toque)"));
        Serial.println(F("  F = Aumentar Farol (OFF -> 40% -> 100%)"));
        Serial.println(F("  G = Diminuir Farol (100% -> 40% -> OFF)"));
        Serial.println(F("  X = Centralizar no Neutro (Imediato)"));
        Serial.println(F("  T = Simulação Automática de 60s"));
        Serial.println(F("  N = Retornar ao modo Rádio Normal"));
        Serial.println(F("  C = Calibração completa"));
        Serial.println(F("  Z = Re-centralizar sticks"));
        Serial.println(F("  P = Imprimir calibração EEPROM"));
        Serial.println(F("  R = Resetar EEPROM"));
        Serial.println(F("  ? = Ajuda\n"));
        break;
    }
  }
}

// ============================================================
// SIMULAÇÃO E TESTES
// ============================================================
void runSimulationStep() {
  if (!g_testActive) return;

  unsigned long elapsed = millis() - g_testStartTime;
  if (elapsed >= 60000) {
    g_testActive = false;
    Serial.println(F("\n[TESTE] Simulação de 60 segundos concluída. Retornando ao modo normal.\n"));
    allLEDsOff();
    return;
  }

  int steerPct = 0;
  int throPct = 0;
  int hlPct = 0;
  const char* desc = "";

  if (elapsed < 5000) { // 0 - 5s
    steerPct = 0; throPct = 0; hlPct = 0;
    desc = "Parado no grid - Faróis Apagados";
  }
  else if (elapsed < 7500) { // 5 - 7.5s
    steerPct = 0; throPct = 0; hlPct = 50;
    desc = "Ligando Faróis - Modo Parcial (40%)";
  }
  else if (elapsed < 10000) { // 7.5 - 10s
    steerPct = 0; throPct = 0; hlPct = 100;
    desc = "Ligando Faróis - Modo Total (100%)";
  }
  else if (elapsed < 15000) { // 10 - 15s
    steerPct = 0; throPct = 50; hlPct = 100;
    desc = "Aceleração Progressiva para Frente";
  }
  else if (elapsed < 25000) { // 15 - 25s
    steerPct = -85; throPct = 20; hlPct = 100;
    desc = "Curva Acentuada para Esquerda";
  }
  else if (elapsed < 30000) { // 25 - 30s
    steerPct = 0; throPct = 90; hlPct = 100;
    desc = "Saída de Curva, Aceleração Forte";
  }
  else if (elapsed < 35000) { // 30 - 35s
    steerPct = 0; throPct = -40; hlPct = 100;
    desc = "Frenagem Brusca - Luzes de Freio Ativas";
  }
  else if (elapsed < 45000) { // 35 - 45s
    steerPct = 85; throPct = -15; hlPct = 100;
    desc = "Ré com Curva para Direita";
  }
  else if (elapsed < 50000) { // 45 - 50s
    steerPct = 0; throPct = 0; hlPct = 100;
    desc = "Parado no Neutro (Faróis FULL)";
  }
  else if (elapsed < 55000) { // 50 - 55s
    steerPct = 0; throPct = 0; hlPct = 50;
    desc = "Reduzindo Faróis para Modo Parcial (40%)";
  }
  else { // 55 - 60s
    steerPct = 0; throPct = 0; hlPct = 0;
    desc = "Desligando Faróis - Fim da Simulação";
  }

  // Converter de percentual para raw baseando-se na calibração
  if (steerPct >= 0) {
    g_simSteer = g_steerCenter + ((long)steerPct * g_cal.steerDeflRight / 100);
  } else {
    g_simSteer = g_steerCenter + ((long)steerPct * g_cal.steerDeflLeft / -100);
  }

  if (throPct >= 0) {
    g_simThro = g_throCenter + ((long)throPct * g_cal.throDeflFwd / 100);
  } else {
    g_simThro = g_throCenter + ((long)throPct * g_cal.throDeflBack / -100);
  }

  g_simHl = g_cal.headlightMin + ((long)hlPct * (g_cal.headlightMax - g_cal.headlightMin) / 100);

  // Print periódico do estado do teste a cada 1 segundo para visualização no monitor serial
  static unsigned long lastSimPrint = 0;
  if (millis() - lastSimPrint >= 1000 || lastSimPrint == 0 || elapsed == 0) {
    lastSimPrint = millis();
    
    // Calcular strings de exibição para coincidir com as decisões de luz correspondentes no loop
    HeadlightMode hlMode = calcHeadlightMode(hlPct);
    bool braking = isBraking(throPct);
    BlinkDirection blinkDir = getBlinkDirection(steerPct);

    Serial.print(F("[TESTE] "));
    Serial.print(elapsed / 1000);
    Serial.print(F("s | "));
    Serial.print(desc);
    Serial.print(F(" | DIR: "));
    if (steerPct >= 0) Serial.print(F("+"));
    Serial.print(steerPct);
    Serial.print(F("% | THR: "));
    if (throPct >= 0) Serial.print(F("+"));
    Serial.print(throPct);
    Serial.print(F("% | HL: "));
    switch (hlMode) {
      case HL_OFF:  Serial.print(F("OFF")); break;
      case HL_DIM:  Serial.print(F("40%")); break;
      case HL_FULL: Serial.print(F("100%")); break;
    }
    Serial.print(F(" | Freio: "));
    Serial.print(braking ? F("ON") : F("OFF"));
    Serial.print(F(" | Pisca: "));
    switch (blinkDir) {
      case BLINK_LEFT:  Serial.println(F("ESQ")); break;
      case BLINK_RIGHT: Serial.println(F("DIR")); break;
      default:          Serial.println(F("---")); break;
    }
  }
}
