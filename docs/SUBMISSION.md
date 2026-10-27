# Submission Guide: Hack for Social Cause, Youth Tech Challenge 2027

## Checklist

- [ ] Every team member registered individually on the MY Bharat portal
- [ ] Team registered under the "Hack for Social Cause" track by the team lead
- [ ] Idea summary submitted ([IDEA_SUMMARY.md](IDEA_SUMMARY.md))
- [ ] Pitch deck / demo video uploaded, if the portal asks for them
- [ ] Institute bonafide certificate uploaded, if required
- [ ] Repo link added to the submission
- [x] Username and contact email filled in across the repo
- [x] Team table filled in the README
- [ ] Rules re-checked on the official portal page (eligibility, deadlines, one team per institute)

## Challenge fit

| Challenge theme | Where it shows up |
|---|---|
| Healthcare & Well-being | Triage engine, telemedicine, medical payloads |
| Disaster Mitigation & Resilience | Flood-aware response, offline edge operation |
| AI, GIS & Emerging Technologies | Edge AI (ECG, YOLOv8), GPS-based dispatch, LoRaWAN |
| Rural Development & Livelihoods | ASHA-worker field unit, rural charging stations |

## Editing the repo after you submit

You can keep changing the repo, because GitHub is separate from the portal. To stay safe:

1. **Tag the submitted version**, so judges can always see exactly what you submitted:
   ```bash
   git tag -a v1.0-submission -m "Version submitted to Hack for Social Cause"
   git push origin v1.0-submission
   ```
2. **Write the tag or commit link in your submission**, for example `https://github.com/GPMINNOVATORS/mission-sanjeevani/releases/tag/v1.0-submission`.
3. **Work on a `dev` branch** after submission and merge to `main` only when tested. A broken `main` looks bad if a judge opens it late.
4. **Check the rules.** Some challenges forbid changes after the deadline or want the code frozen. If the portal says so, only push to `dev` until results are out.
5. **Never rewrite history** (`git push --force`) on `main`.
6. Whether the portal lets you edit your *application* after submitting is decided by the portal, not GitHub. Check on your dashboard.
