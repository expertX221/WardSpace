# Architecture and implementation

## Flow

Browser synthetic sensors (3 seconds) → local durable outbox → POST /api/events → server validation/risk assessment → Neon Postgres → API acknowledgment. Browser risk rules provide immediate offline feedback → one open alert episode → caregiver acknowledgment → simulated response event. The UI uses local state for immediate rendering; server recalculation is stored for audit comparison.

Local alternative: the same UI → Python HTTP handler → SQLite. Cloud: Vercel static assets + Node serverless function + pg connection pool attached to Vercel lifecycle + Neon pooled TLS connection.

## Scene matrix

| Surface | Purpose | Scene and interaction | Fallback |
|---|---|---|---|
| Overview / | Monitor a synthetic patient | Blender bedroom, orbit, zoom, breathing blanket, gateway rings | CSS 3D bedroom |
| Bed camera preset | Inspect patient sensor | Camera targets bed, heart hotspot scrolls to vital | Vital cards remain available |
| Gateway preset | Explain sensor ingestion | Camera targets gateway, hotspot focuses offline simulation | Gateway status and outbox count |
| Care timeline | Close the response loop | Semantic controls adjacent to the scene | Full keyboard-operable HTML |

## Event schema

Each event has UUID `id`, random browser `session`, `type`, timestamp `at`, `data`, latest `note`. Server adds `receivedAt` and recalculated `risk` for readings. Types: reading, note, attendance, acknowledge, response. Postgres enforces unique event IDs. Retries return the original record. Parameterized SQL prevents query injection. Payload limit is 16KB. Readings validate finite numerical values and plausible demonstration ranges.

## Explainable rules v1

Oxygen below 92: +4; heart rate outside 50–110: +2; respiration outside 10–24: +2; temperature ≥38: +2; systolic pressure below 90: +3. A supported non-negated note keyword adds +2. Scores 0–1 Low, 2–3 Medium, ≥4 High. This is a deterministic baseline, not a trained ML model. Python, browser and cloud functions mirror the rules. Negation is limited to a small pattern and is not general clinical NLP.

No learning dataset is required: sensor data is generated in the browser. Synthetic examples are in `data/scenarios.csv`. These examples are not a performance evaluation dataset.

## Reliability

Browser localStorage saves the queue before network submission. Sequential replay and primary-key idempotency cover interrupted responses. Failed requests remain queued. Power outage stops synthetic generation; data older than ten seconds is marked stale. Service worker caches the application on first successful visit; browser reload during network loss can use cached assets. Gateway failure is simulated while browser compute remains available. Closing the browser stops collection and escalation timers. The app does not simulate an actual UPS.

## Limits and future work

No identity verification, remote caregiver device, background delivery, diagnosis or clinically validated prediction. A 24–48 hour model requires longitudinal labeled patient data, leakage-safe temporal splits, calibration, subgroup evaluation, prospective validation and clinician-defined escalation protocols. Production also needs access control, ingestion quotas, encryption/retention policy, trusted sensor timestamps and robust note interpretation.
