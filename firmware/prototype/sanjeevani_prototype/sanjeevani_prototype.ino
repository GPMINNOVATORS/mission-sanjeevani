#include <LiquidCrystal.h>
#include <Servo.h>

// ---- CHANGED: Moved last pin from 1 to 8 to avoid Serial TX conflict ----
// Pins sequence: RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 10, 9, 13, 8);

// ---- PINS CONFIGURATION ----
const int potPin = A0;       // Weight Simulator (Potentiometer Middle Pin)
const int sosButton = 2;     // Emergency SOS Switch (Push Button)
const int servoPin = 3;      // MG995 Servo Motor Signal
const int trigPin = 4;       // Ultrasonic Sensor Trig Pin
const int echoPin = 5;       // Ultrasonic Sensor Echo Pin
const int greenLed = 6;      // Ready Status LED
const int redLed = 7;        // Emergency Status LED
const int buzzer = A1;       // Buzzer on Analog A1

Servo lockServo;
int systemState = 0;         // 0 = Idle/Pre-flight, 1 = In Flight, 2 = Arrived/Drop Zone
float payloadWeight = 0;
float lastWeight = -1;

void setup() {
  // Serial Monitor Initialization
  Serial.begin(9600);
  Serial.println(F("========================================="));
  Serial.println(F("    SANJEEVANI DRONE SYSTEM INITIALIZED  "));
  Serial.println(F("========================================="));
  Serial.println(F("Commands: 'START' to takeoff, 'DROP' to release cargo, 'RESET' to return home."));

  // LCD Initialization
  lcd.begin(16, 2);
  lcd.clear();
  lcd.print("MISSION:");
  lcd.setCursor(0, 1);
  lcd.print("SANJEEVANI READY");

  // ---- CHANGED: Input Pullup stops the button from floating into an infinite loop ----
  pinMode(sosButton, INPUT_PULLUP); 
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(buzzer, OUTPUT);

  // Servo Initialization (Locked Position initially)
  lockServo.attach(servoPin);
  lockServo.write(0); // 0 degrees = Locked
  
  // Set initial LED state
  digitalWrite(greenLed, HIGH);
  digitalWrite(redLed, LOW);
}

void loop() {
  // 1. Read Payload Weight (Potentiometer Simulation)
  int potValue = analogRead(potPin);
  payloadWeight = (potValue / 1023.0) * 5.0; // Scaled to simulate 0-5 kg cargo

  // Print weight to Serial only if it changes significantly
  if (abs(payloadWeight - lastWeight) > 0.1) {
    Serial.print(F("[SANJEEVANI] Payload Weight: "));
    Serial.print(payloadWeight, 2);
    Serial.println(F(" kg"));
    lastWeight = payloadWeight;
  }

  // 2. Read Ultrasonic Distance (Altitude Simulation)
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1; // Distance in cm

  // 3. Handle SOS Hardware Button Press 
  // ---- CHANGED: Triggers when pulled to LOW (pressed) ----
  if (digitalRead(sosButton) == LOW) {
    handleEmergency();
  }

  // 4. Check for Serial Commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); 
    command.toUpperCase();

    if (command == "START") {
      if (systemState == 0) {
        takeoffSequence();
      } else {
        Serial.println(F("[ERROR] Drone is already airborne or has arrived."));
      }
    } 
    else if (command == "DROP") {
      if (systemState == 1 || systemState == 2) {
        releasePayloadSequence();
      } else {
        Serial.println(F("[ERROR] Cannot drop. Drone is still grounded."));
      }
    } 
    else if (command == "RESET") {
      resetSystem();
    }
  }

  // 5. Update Status-dependent Displays
  updateDisplays(distance);
  delay(200); // Small stability delay
}

// ---- MISSION STATE CONTROL FUNCTIONS ----

void takeoffSequence() {
  systemState = 1; // Flight mode
  Serial.println(F("\n>>> [MISSION SANJEEVANI] TAKEOFF APPROVED. EN ROUTE..."));
  
  // Flash green LED to signify takeoff
  for(int i=0; i<3; i++) {
    digitalWrite(greenLed, LOW); delay(200);
    digitalWrite(greenLed, HIGH); delay(200);
  }
  
  lcd.clear();
  lcd.print("STATE: EN ROUTE");
}

void releasePayloadSequence() {
  systemState = 2; // Arrived / Dropped
  Serial.println(F("\n>>> [MISSION SANJEEVANI] REACHED DROP ZONE. RELEASING PAYLOAD..."));
  
  lcd.clear();
  lcd.print("DROPPING CARGO...");
  
  // Unlocking servo mechanism
  lockServo.write(90); // Rotate to 90 degrees to unlock cargo latch
  
  // Sound buzzer to alert ground crew
  digitalWrite(buzzer, HIGH);
  delay(1000);
  digitalWrite(buzzer, LOW);
  
  Serial.println(F(">>> [SUCCESS] CARGO DISPATCHED SUCCESSFULLY."));
  lcd.setCursor(0, 1);
  lcd.print("DISPATCHED!");
}

void handleEmergency() {
  Serial.println(F("\n [EMERGENCY] SOS TRIGGERED OVER SERIAL/HARDWARE! ABORTING MISSION!"));
  digitalWrite(redLed, HIGH);
  digitalWrite(greenLed, LOW);
  
  lcd.clear();
  lcd.print("!! EMERGENCY !!");
  lcd.setCursor(0, 1);
  lcd.print("MISSION ABORTED");
  
  // Pulsing Alarm tone
  for(int i = 0; i < 5; i++) {
    digitalWrite(buzzer, HIGH); delay(100);
    digitalWrite(buzzer, LOW); delay(100);
  }
}

void resetSystem() {
  systemState = 0;
  lockServo.write(0); // Relock servo
  digitalWrite(redLed, LOW);
  digitalWrite(greenLed, HIGH);
  lastWeight = -1;
  
  Serial.println(F("\n>>> [SYSTEM RESET] Sanjeevani Drone back on Launchpad."));
  lcd.clear();
  lcd.print("MISSION: SANJEEVANI");
  lcd.setCursor(0, 1);
  lcd.print("STATUS: READY");
}

void updateDisplays(long altitude) {
  // Update LCD dynamically depending on current flight state
  if (systemState == 1) {
    lcd.setCursor(0, 0);
    lcd.print("Alt: ");
    lcd.print(altitude);
    lcd.print(" cm   "); 
    
    lcd.setCursor(0, 1);
    lcd.print("Wt: ");
    lcd.print(payloadWeight, 1);
    lcd.print("kg Flight  ");
  }
}
