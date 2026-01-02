# ADCS Derivation of Gyroscopic Factor

## Goal
Derive a mapping from attitude control authority (CMG/RW dynamics and control gains) to a scalar gyroscopic factor `G_factor` used in the prototype.

## Notation
- q(t): attitude quaternion
- ω_g: gyroscope spin vector (rad/s)
- I: inertia tensor
- τ_ctrl: control torque from CMGs/RWs
- K_ctrl: effective control gain (N·m/rad)
- G: scalar proxy for gyroscope spin magnitude

## Linearized attitude error dynamics
1. Start from rotational dynamics: \(I\dot{\omega} + \omega \times I\omega = \tau_{\text{ctrl}} + \tau_{\text{ext}}\).
2. Linearize about nominal spin and small attitude error δθ.
3. Express closed-loop error dynamics under PD or LQR control.

## Mapping to `G_factor`
1. Define control authority metric \(A(G) \propto K_{\text{ctrl}} G^2 / I_{\text{eff}}\).
2. Normalize to a bounded factor: propose \( \mathcal{G} = 1 / \sqrt{1 + \kappa / G^2} \) with \(\kappa = I_{\text{eff}}/K_{\text{ctrl}}\).
3. Discuss limitations and how to replace with a full simulation-based lookup table.

## Validation plan
- Compare linearized prediction to a high-fidelity quaternion + CMG simulation for a set of G values.
- Fit parameters (I_eff, K_ctrl) to match control authority curves.

## References
- [Reference texts on spacecraft attitude control and CMG dynamics]
