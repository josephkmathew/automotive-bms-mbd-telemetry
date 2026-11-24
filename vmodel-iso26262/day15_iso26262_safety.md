# Day 15: ISO 26262 Functional Safety Mapping (BMS Protection & SoC)

## 1. HARA & ASIL Context (ASIL A to D)
- **Automotive Safety Integrity Level (ASIL)** is determined by three factors:
  - **Severity (S):** Potential harm if a failure occurs (e.g., thermal runaway from cell over-voltage).
  - **Exposure (E):** Probability of the vehicle being in the operational situation.
  - **Controllability (C):** Ability of the driver or system to avoid harm once the fault occurs.
- High-voltage EV battery protection typically targets **ASIL C or ASIL D** due to severe thermal/electrical hazard consequences.

## 2. Mapping BMS_Protection_SoC to Safety Mechanisms
| Safety Concept | Implementation in `BMS_Protection_SoC.slx` | Verification Evidence (`run_bms_mil_tests.m`) |
| :--- | :--- | :--- |
| **Safe Operating Area (SOA)** | Normal state operates strictly within `3.0 V <= voltage <= 4.2 V` (`fault = 0`) | `Normal_Window` test case verifies `fault` remains `0` |
| **Over-Voltage Detection & Safe State** | Transition `[voltage > 4.2]` enters `OverVoltage_Fault` (`fault = 1`) | `OverVoltage_Entry` test case verifies transition to `fault = 1` |
| **Under-Voltage Detection & Safe State** | Transition `[voltage < 3.0]` enters `UnderVoltage_Fault` (`fault = 2`) | `UnderVoltage_Entry` test case verifies transition to `fault = 2` |
| **Traceable Verification** | Automated batch script logs signals and checks pass/fail criteria | `bms_mil_results.csv` and `bms_mil_results.mat` |

## 3. Engineering Trade-Offs to Highlight in Interviews
- **Hysteresis / Debouncing:** Real BMS controllers add voltage hysteresis and debounce timers before clearing faults so sensor noise near `3.0 V` or `4.2 V` does not cause rapid state chattering.
- **Plausibility & Sensor Diagnostics:** Production ISO 26262 designs also check for open-wire/short-to-ground sensor faults and cross-check Coulomb-counted SoC against Open-Circuit Voltage (OCV) lookup tables to prevent drift.
