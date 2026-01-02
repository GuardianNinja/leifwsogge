# Lambda Prototype — 10‑Year Monte‑Carlo

## Overview

This repository contains a prototype simulation for a scalar diagnostic relation used to evaluate a spacecraft-like trajectory/stability concept:



\[
\Lambda = 2 \left(\frac{\Omega R}{\alpha \,\mathcal{G}}\right)^2 \frac{v}{t_p}
\]




Where:

- **\(\Omega\)**, **\(\alpha\)** are scale parameters (unitless in the prototype).
- **\(R\)** is a relativity factor (set to 1 for nonrelativistic runs).
- **\(\mathcal{G}\)** is a gyroscopic/ADCS factor derived from a simple linearized model.
- **\(v\)** is relative speed (m/s).
- **\(t_p\)** is the "place-in-time" timestamp in seconds (08:43 → 31380 s in the prototype).
- **\(\Lambda\)** is a regularized finite scale replacing the sketch's literal infinity.


## Files

- `simulate_lambda.py` — main simulation script (10-year Monte-Carlo).
- `requirements.txt` — Python dependencies.
- `run_example.sh` — convenience script to run the simulation.
- `simulation_outputs/` — generated PNGs and `summary.csv` after running.

## How to run

1. Create a virtual environment (recommended).
2. Install dependencies:
