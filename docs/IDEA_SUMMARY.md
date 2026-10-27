# Idea Summary (for the MY Bharat portal form)

Copy and edit these answers for the submission form. Shorten to fit any character limits.

**Project name:** Mission Sanjeevani

**Theme:** Healthcare & Well-being (also: Disaster Mitigation & Resilience; AI, GIS & Emerging Technologies)

**Problem statement:**
In rural and flood-prone areas such as parts of Bihar, poor roads and distant hospitals delay emergency care. In road accidents, snakebites and pregnancy complications, the first hour decides the outcome, yet help often arrives late, patient information does not reach doctors, and cloud-only systems fail when network coverage is weak.

**Proposed solution:**
An AIoT emergency response network with four connected parts:
1. A **field unit**, used by an ASHA worker, captures vitals (ECG, SpO₂, temperature) and GPS location.
2. A **triage engine** scores urgency (GREEN to RED) so the most critical patients are prioritised.
3. A **dispatch planner** picks the nearest drone with enough battery and the right medical kit. Restricted medicines are released only after remote doctor authorisation.
4. **Telemedicine** lets a doctor guide the patient or ASHA worker while the drone is on its way.

Data travels over LoRaWAN or 4G/5G, and processing happens at the edge (Raspberry Pi / Jetson Nano) so the system works with weak connectivity.

**Technology used:** IoT sensors, ESP32, Raspberry Pi 4, Jetson Nano, LoRaWAN, edge AI (ECG analysis, YOLOv8 landing-zone detection), Python, drones.

**Current status (honest):**
Working: control-logic prototype, rule-based triage, dispatch planner, LoRaWAN payload format, web dashboard. Under development and testing: AI-based ECG analysis, YOLOv8 landing detection, real field-unit hardware, flight tests.

**Social impact / how we measure it:**
Time from SOS to first help (drone vs road), triage agreement with doctors, dispatch success rate, and number of cases reached that roads could not serve during floods. See `docs/IMPACT.md`.

**Scalability:** Solar-hybrid rural charging stations and multi-drone fleets can create distributed response nodes across districts.

**Code repository:** https://github.com/GPMINNOVATORS/mission-sanjeevani
