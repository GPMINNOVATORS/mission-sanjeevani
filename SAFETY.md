# Safety & Responsible Use

Mission Sanjeevani deals with human health. Please read before using or deploying.

1. **Not a medical device.** The code is a research prototype and has not been clinically validated or certified.
2. **Triage thresholds are placeholders.** The vitals scoring is modelled on public early-warning-score conventions and must be reviewed by licensed clinicians for the target population (including children and pregnant patients, who need different ranges).
3. **Payloads need protocol.** Kit contents, cold-chain handling (e.g. for antivenom) and who may authorise release must follow state health-department protocols and law.
4. **Aviation law.** Drone operations must comply with India's DGCA Drone Rules, including BVLOS permissions, no-fly zones and airworthiness.
5. **Human in the loop.** The system supports clinicians and health workers. It never replaces them. High-risk actions require remote doctor authorisation.
6. **Data privacy.** Patient data is sensitive. Follow applicable law (e.g. India's DPDP Act, 2023), minimise collection, encrypt in transit and at rest, and de-identify any data used for model training.
7. **Fallback always.** If no drone is viable, the system must direct the user to ambulance services (108/102) and local helplines.

Found a safety or security issue? See [SECURITY.md](SECURITY.md).
