# Roadmap

## Now: IoT prototype + connected architecture
- [x] Control-logic prototype (Arduino/Tinkercad)
- [x] Rule-based triage and dispatch planner
- [x] LoRaWAN payload codec
- [x] Web control-room dashboard
- [x] Response-time comparison model
- [ ] Fix prototype issues ([PROTOTYPE_NOTES.md](PROTOTYPE_NOTES.md))
- [ ] ESP32 field unit with real sensors (ECG, SpO₂, temperature, GPS)
- [ ] MQTT broker + FastAPI mission-control backend

## Next: AI modules (under implementation & testing)
- [ ] ECG classification model, benchmarked against the rule-based baseline
- [ ] YOLOv8 landing-pad detection dataset and model
- [ ] Offline inference on Jetson Nano / Pi 4

## Then: Edge AI + advanced ECG analytics
- [ ] Model optimisation (TensorRT / quantisation)
- [ ] Clinician-reviewed decision-support rules

## Scale: Multi-drone fleet + smart routing
- [ ] Fleet manager, flood-aware routing, no-fly zones, weather checks
- [ ] MAVLink integration (PX4 / ArduPilot)

## Expand: Solar-hybrid rural charging stations
- [ ] Distributed response nodes in rural areas
