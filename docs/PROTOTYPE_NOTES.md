# Prototype Notes: Known Issues & Next Steps

Observations from reviewing `sanjeevani_prototype.ino`. The original file is kept unchanged. These are good first issues for contributors.

| # | Issue | Suggested fix |
|---|---|---|
| 1 | `pulseIn(echoPin, HIGH)` has no timeout and can block for about 1 s if no echo returns. | `pulseIn(echoPin, HIGH, 30000)` and treat 0 as "out of range". |
| 2 | SOS never changes `systemState`. The alarm repeats every loop while the button is held, and the servo is not affected. | Add `STATE_ABORTED`, latch the SOS, and require `RESET` to clear it. |
| 3 | The message says "SOS TRIGGERED OVER SERIAL/HARDWARE", but there is no serial SOS command. | Add an `SOS` serial command or fix the message. |
| 4 | `resetSystem()` prints `MISSION: SANJEEVANI` (19 chars) on a 16-column LCD, so it is truncated. | Shorten to `SANJEEVANI` / `STATUS: READY`. |
| 5 | `DROP` is allowed repeatedly in state 2 and ignores payload weight. | Reject a second `DROP`. Require weight above a threshold before takeoff. |
| 6 | `delay()` in the takeoff and drop sequences blocks input, including SOS. | Use `millis()`-based non-blocking timing. |
| 7 | `Serial.readStringUntil('\n')` can stall for 1 s if no newline arrives. | Set `Serial.setTimeout(50)` or parse char by char. |
| 8 | Weight comes from a potentiometer and altitude from an ultrasonic sensor. | Real hardware: HX711 load cell for weight, barometer + GPS (from the flight controller) for altitude. |

## Bridging the prototype to the rest of the system

1. Replace serial commands with messages from the edge computer (MQTT or LoRaWAN downlink).
2. Gate `DROP` on a **doctor-authorisation flag** for restricted payloads (see `src/sanjeevani/dispatch.py`).
3. Publish telemetry (state, weight, altitude) back to mission control using the compact payload format in `src/sanjeevani/lora_payload.py`.
