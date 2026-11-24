# Day 14: Automotive V-Model Traceability Mapping

## V-Model Mapping Table

| V-Model Stage | Side / Level | Project Artifact / Logic | Purpose & Verification Role |
| :--- | :--- | :--- | :--- |
| **System & Safety Requirements** | Left — Top | BMS voltage limits (`3.0 V`–`4.2 V`), fault codes (`0`, `1`, `2`), and current integration SoC logic | Defines expected cell protection and State of Charge tracking behavior before modeling |
| **Architectural & Detailed Design** | Left — Middle/Bottom | `BMS_Protection_SoC.slx`, `Stateflow_Transmission_Logic.slx`, `Vehicle_Cruise_Control.slx`, `ABS_Simulation_Completed.slx` | Implements Stateflow fault state transitions and continuous/discrete control & SoC signal flows |
| **Model-in-the-Loop (MIL) Verification** | Right — Bottom | `run_bms_mil_tests.m`, `bms_mil_results.mat`, `bms_mil_results.csv` | Automates edge-case scenarios (`UnderVoltage_Entry`, `Normal_Window`, `OverVoltage_Entry`, `ZeroCurrent_Check`) and logs pass/fail results |
| **SIL / HIL / Vehicle Validation** | Right — Middle/Top (Next Phases) | Generated code / hardware rig / CAN telemetry (`cantools`, `pandas`, `matplotlib`) | Extends MIL logic to software-in-the-loop, hardware-in-the-loop, and real/simulated CAN log analysis |

## Key Takeaways for Day 14
- **Left side (Decomposition):** Translates voltage/current protection and SoC requirements into Simulink blocks and Stateflow states.
- **Right side (Verification & Validation):** Uses automated MIL runs (`run_bms_mil_tests.m`) to confirm that `fault` states and `SoC` outputs match expectations across edge cases.
