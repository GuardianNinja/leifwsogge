#!/usr/bin/env python3
"""
simulate_lambda.py

10-year Monte-Carlo prototype for the scalar relation:
plt.ylabel("Lambda (numeric scale)")  # type: ignore

Key features:
- Explicit units documented in comments.
- Derived-ish gyroscopic factor from a simple linearized ADCS model:
    G_factor = 1 / sqrt(1 + kappa / G^2)
  where kappa = I_eff / K_ctrl (I_eff: effective inertia, K_ctrl: control gain).
- Orientation error modeled as AR(1) and modifies G_factor multiplicatively.
- CMG momentum capacity, desaturation events, fuel budget, and failure detection.
- N Monte-Carlo trials, vectorized where reasonable.
- Saves PNG plots: lambda_timeseries.png, G_v_example.png, lambda_histogram.png.

Run:
    python simulate_lambda.py
"""


try:
    import numpy as np
except ImportError:
    raise ImportError("numpy is required for this script. Please install it with 'pip install numpy'.")
try:
    import matplotlib.pyplot as plt  # type: ignore
except ImportError:
    raise ImportError("matplotlib is required for plotting. Please install it with 'pip install matplotlib'.")
try:
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for CSV output. Please install it with 'pip install pandas'.")
except ImportError:
    raise ImportError("pandas is required for CSV output. Please install it with 'pip install pandas'.")
from pathlib import Path


# -------------------------
# Simulation parameters
# -------------------------
np.random.seed(42)  # type: ignore[attr-defined]

# Time
DAYS_PER_YEAR = 365
YEARS = 10
DAYS = DAYS_PER_YEAR * YEARS  # 3650
DT = 1.0  # days (timestep)

# Timestamp (place-in-time) used as t_p (seconds since midnight)
# 08:43 -> 8*3600 + 43*60 = 31380 s
t_p = 31380.0  # seconds

# Physical / model parameters (units noted)
Omega = 1.0        # unitless scale factor
alpha = 1.0        # unitless
R = 1.0            # relativity factor (nonrelativistic here)
# If you need relativistic regime, replace R with gamma(v) where appropriate.

# Gyroscope / ADCS parameters
I_eff = 50.0       # kg·m^2 (effective inertia used to form kappa)
K_ctrl = 0.1       # control gain (N·m/rad or equivalent)
kappa = I_eff / K_ctrl  # dimension: same as (G^2) to make G_factor dimensionless

G0 = 10.0          # rad/s reference (not used directly in derived factor)
G_init = 100.0     # rad/s initial gyroscope spin
# Drift: fractional per year (e.g., -0.005 means -0.5% per year)
G_drift_frac_per_year = -0.005
G_drift_frac_per_day = G_drift_frac_per_year / DAYS_PER_YEAR

sigma_G = 1.0      # rad/s daily noise on G

# Orientation error AR(1)
phi = 0.995
eps_sigma = 0.05

# Velocity model
v_init = 7500.0    # m/s initial orbital-like speed
sigma_v = 0.5      # m/s daily random walk

# CMG / momentum capacity and desaturation
G_max = 500.0      # rad/s (capacity)
G_min_weak = 20.0  # rad/s threshold for weak stabilization
desat_threshold = 0.9 * G_max
fuel_budget_init = 1000  # arbitrary units
fuel_per_desat = 10

# Monte-Carlo
N_TRIALS = 100

# Output directory
OUTDIR = Path("simulation_outputs")
OUTDIR.mkdir(exist_ok=True)

# -------------------------
# Helper functions
# -------------------------
def gyroscopic_factor(G: float, kappa: float) -> float:
    """
    Derived-ish gyroscopic factor from a linearized ADCS model.
    G_factor = 1 / sqrt(1 + kappa / G^2)
    - G: gyroscope spin (rad/s)
    - kappa: I_eff / K_ctrl (dimension consistent with G^2)
    Returns a dimensionless factor in (0,1].
    """
    return 1.0 / np.sqrt(1.0 + kappa / (G ** 2))  # type: ignore[no-untyped-call]

def compute_lambda(Omega: float, R: float, alpha: float, G_factor_eff: float, v: float, t_p: float) -> float:
    """
    Compute Lambda per the regularized scalar relation.
    Units: depends on how you interpret Lambda. Here we return a numeric scale.
    """
    return 2.0 * ((Omega * R) / (alpha * G_factor_eff)) ** 2 * (v / t_p)

# -------------------------
# Simulation loop (Monte-Carlo)
# -------------------------
# Pre-allocate arrays
lambda_all = np.zeros((N_TRIALS, DAYS)) # pyright: ignore[reportUnknownMemberType]
G_all = np.zeros((N_TRIALS, DAYS)) # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
v_all: np.ndarray = np.zeros((N_TRIALS, DAYS)) # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
desat_counts: np.ndarray = np.zeros(N_TRIALS, dtype=int)  # type: ignore[reportUnknownVariableType]
saturation_counts = np.zeros(N_TRIALS, dtype=int) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
weak_days_counts = np.zeros(N_TRIALS, dtype=int) # pyright: ignore[reportUnknownVariableType]
failure_flags = np.zeros(N_TRIALS, dtype=bool) # pyright: ignore[reportUnknownMemberType]

for trial in range(N_TRIALS):
    g: float = float(G_init)
    v_curr: float = float(v_init)
    e_t: float = 0.0
    fuel = fuel_budget_init
    cumulative_momentum = 0.0  # proxy for momentum usage
    desat_count = 0
    sat_count = 0
    weak_count = 0
    failed = False

    for day in range(DAYS):
        # Apply drift (fractional) and noise to g
        g: float = g * (1.0 + G_drift_frac_per_day)
        g = g + float(np.random.normal(0.0, sigma_G))  # type: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        g = max(g, 0.01)  # prevent zero or negative

        # Orientation error AR(1)
        eps: float = float(np.random.normal(0.0, eps_sigma))  # type: ignore[attr-defined, arg-type]
        e_t = float(phi * float(e_t) + eps)

        # Derived gyroscopic factor and effective factor with orientation error
        G_factor = gyroscopic_factor(g, kappa)
        G_factor_eff: float = float(G_factor * (1.0 - 0.01 * float(e_t)))  # ensure float type

        # Compute Lambda
        lam = compute_lambda(Omega, R, alpha, G_factor_eff, float(v_curr), t_p)

        # Record
        lambda_all[trial, day] = lam
        G_all[trial, day] = g
        v_all[trial, day] = v_curr

        # Update v (random walk)
        v_curr: float = v_curr + float(np.random.normal(0.0, sigma_v))  # type: ignore[attr-defined, arg-type]

        # Track weak stabilization
        if g < G_min_weak:
            weak_count += 1

        # Saturation handling
        if g > G_max:
            sat_count += 1
            g = G_max  # cap

        # Momentum accumulation heuristic: use g as proxy for momentum
        cumulative_momentum += abs(g) * 0.001  # arbitrary scaling to accumulate over time

        # Desaturation policy
        if cumulative_momentum >= desat_threshold:
            # perform desaturation if fuel available
            if fuel >= fuel_per_desat:
                fuel -= fuel_per_desat
                desat_count += 1
                cumulative_momentum = 0.0
                g = G_init  # reset spin after desat
            else:
                # failure due to no fuel for desaturation
                failed = True
                failure_flags[trial] = True
                break

    desat_counts[trial] = desat_count
    saturation_counts[trial] = sat_count
    weak_days_counts[trial] = weak_count
    failure_flags[trial] = failed

# -------------------------
# Aggregate statistics
# -------------------------
lambda_mean = np.mean(lambda_all)
lambda_mean: float  # type: ignore[assignment, reportUnknownMemberType]
lambda_std = np.std(lambda_all)
lambda_min = np.min(lambda_all) # pyright: ignore[reportUnknownMemberType]
lambda_min: float  # type: ignore[assignment]
lambda_max = np.max(lambda_all) # pyright: ignore[reportUnknownMemberType]
lambda_max: float = float(lambda_max)  # type: ignore[assignment]
lambda_std: float  # type: ignore[assignment]

from typing import Dict, Any
summary: Dict[str, Any] = {
    "lambda_mean": lambda_mean,
    "lambda_std": lambda_std,
    "lambda_min": lambda_min,
    "lambda_max": lambda_max,
    "total_saturation_events": int(np.sum(saturation_counts)),  # type: ignore[reportUnknownMemberType, reportUnknownArgumentType]
    "total_desat_events": int(np.sum(desat_counts)), # pyright: ignore[reportUnknownMemberType]
    "total_weak_days": int(np.sum(np.asarray(weak_days_counts))), # pyright: ignore[reportUnknownMemberType]
    "failures": int(np.sum(failure_flags)), # pyright: ignore[reportUnknownMemberType] # pyright: ignore[reportUnknownArgumentType] # pyright: ignore[reportUnknownArgumentType]
}

# Print summary
print("=== 10-year Monte-Carlo Summary ===")


from typing import Any
for k, v in summary.items(): # pyright: ignore[reportUnknownVariableType]
    # Explicitly annotate v as Any to satisfy type checkers
    v: Any
    print(f"{k}: {v}")

# -------------------------
# Plots
# -------------------------
# 1) Lambda time series: median and 10/90 percentiles across trials
lambda_median = np.median(lambda_all, axis=0) # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
lambda_median: np.ndarray  # type: ignore[assignment]
lambda_p10 = np.percentile(lambda_all, 10, axis=0)  # type: ignore[reportUnknownMemberType]
lambda_p90 = np.percentile(lambda_all, 90, axis=0)  # type: ignore[reportUnknownMemberType]
days: np.ndarray = np.arange(DAYS)  # type: ignore[reportUnknownMemberType]


plt.figure(figsize=(10, 5))  # type: ignore[reportUnknownMemberType]
plt.fill_between(days, lambda_p10, lambda_p90, color="lightgray", label="10-90 percentile")  # type: ignore
plt.xlabel("Day") # pyright: ignore[reportUnknownMemberType]
plt.ylabel("Lambda (numeric scale)")  # type: ignore[reportUnknownMemberType]
plt.title("Lambda over 10 years (median and 10/90 percentiles)")  # type: ignore
plt.legend()  # type: ignore
plt.grid(True)  # type: ignore
plt.tight_layout()  # type: ignore
plt.savefig(OUTDIR / "lambda_timeseries.png", dpi=150)  # type: ignore
plt.close('all')  # type: ignore[reportUnknownMemberType]

# 2) Example single-trial time series of G and v (trial 0)
plt.figure(figsize=(10, 5)) # pyright: ignore[reportUnknownMemberType]
ax1 = plt.gca()  # type: ignore
ax1.plot(days, G_all[0], color="C1", label="G (rad/s)")  # type: ignore
ax1.set_xlabel("Day")  # type: ignore
ax1.set_ylabel("G (rad/s)", color="C1")  # type: ignore
ax1.tick_params(axis="y", labelcolor="C1")  # type: ignore
ax2 = ax1.twinx()  # type: ignore[reportUnknownMemberType]
ax2.plot(days, v_all[0], color="C2", label="v (m/s)", alpha=0.7)  # type: ignore
ax2.set_ylabel("v (m/s)", color="C2")  # type: ignore
ax2.tick_params(axis="y", labelcolor="C2")  # type: ignore
plt.title("Example trial: G and v over time (trial 0)")  # type: ignore
ax1.grid(True)  # type: ignore
plt.tight_layout()  # type: ignore
plt.savefig(OUTDIR / "G_v_example.png", dpi=150)  # type: ignore
plt.close('all')  # type: ignore[reportUnknownMemberType]

# 3) Histogram of Lambda values across all trials and days

plt.figure(figsize=(8, 5))  # type: ignore
plt.hist(lambda_all.flatten(), bins=100, color="C3", alpha=0.8)  # type: ignore
plt.xlabel("Lambda")  # type: ignore
plt.ylabel("Frequency")  # type: ignore
plt.title("Histogram of Lambda values (all trials & days)")  # type: ignore
plt.grid(True)  # type: ignore
plt.tight_layout()  # type: ignore
plt.savefig(OUTDIR / "lambda_histogram.png", dpi=150)  # type: ignore
plt.close() # pyright: ignore[reportUnknownMemberType]

# Save a small CSV summary for inspection
df_summary = pd.DataFrame({
    "lambda_mean": [lambda_mean],
    "lambda_std": [lambda_std],
    "lambda_min": [lambda_min],
    "lambda_max": [lambda_max],
    "total_saturation_events": [summary["total_saturation_events"]],
    "total_desat_events": [summary["total_desat_events"]],
    "total_weak_days": [summary["total_weak_days"]],
    "failures": [summary["failures"]],
})
df_summary.to_csv(OUTDIR / "summary.csv", index=False)  # type: ignore

print(f"Plots and summary saved to {OUTDIR.resolve()}")
