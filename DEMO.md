# Recorded walkthrough

Watch: https://wardspace-healthcare.vercel.app/demo.html

Direct MP4: https://wardspace-healthcare.vercel.app/demo.mp4

Captioned three-minute recording of the live demo presentation. No voiceover. All patient data is synthetic. The presentation layer records the actual 3D renderer and current DOM telemetry; scheduled actions operate the application controls.

# Three-minute recording script

0:00–0:25 — Show the Blender room and explain the problem: at-home patients lack continuous oversight. Orbit the scene; show the breathing blanket and gateway signals. State that all data is synthetic.

0:25–0:50 — Show the five live readings, sparkline history and the sensor hotspots. Explain the complete flow from software sensors to platform and persisted events.

0:50–1:20 — Choose Deterioration. Show falling oxygen and increasing heart/respiratory rates. Read the explicit risk reasons. Explain that the rules are an interpretable baseline and the 24–48h panel is exploratory, not a validated prediction.

1:20–1:50 — Check in as the caregiver. Save an English note such as “Patient feels dizzy.” Show the score updating. Acknowledge the alert and record a simulated response. Point out the stored audit events.

1:50–2:20 — Simulate offline. Show the outbox increasing while risk scoring continues. Reconnect and show the pending count dropping to zero. Demonstrate power outage; wait for the stale-data label; restore power.

2:20–2:45 — Select Recovery. Explain that an existing alert still requires a human response. Download history. Show Neon event persistence if cloud deployed.

2:45–3:00 — Show source repository, Blender file and technical documentation. State the limits: no real emergency messaging, no real patient data, no validated diagnosis or 24–48h prediction. Finish with Sense → Understand → Predict → Alert → Respond.
