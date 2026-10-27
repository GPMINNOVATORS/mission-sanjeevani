# Control-Logic Prototype (Arduino / Tinkercad)

The payload-bay and mission-state logic from our demo video. It is a **simulation of the control logic**, not flight firmware.

Open `sanjeevani_prototype/sanjeevani_prototype.ino` in the Arduino IDE, or paste it into a Tinkercad Circuits Arduino Uno project.

## Wiring

| Pin | Part | Simulates |
|---|---|---|
| 12, 11, 10, 9, 13, 8 | 16x2 LCD (RS, E, D4–D7) | Status display |
| A0 | Potentiometer | Payload weight, 0–5 kg |
| 2 | Push button (`INPUT_PULLUP`) | Emergency SOS |
| 3 | MG995 servo | Cargo latch (0° locked, 90° released) |
| 4 / 5 | HC-SR04 trig / echo | Altitude, in cm |
| 6 / 7 | Green / red LED | Ready / emergency |
| A1 | Buzzer | Ground-crew alert |

## Serial commands (9600 baud)

`START` takeoff, `DROP` release cargo, `RESET` back to launchpad.

## State machine

`0 IDLE` →(START)→ `1 IN FLIGHT` →(DROP)→ `2 DROPPED` →(RESET)→ `0 IDLE`. The SOS button can be pressed in any state.

Known issues and suggested next steps are in [docs/PROTOTYPE_NOTES.md](../../docs/PROTOTYPE_NOTES.md).
