# README — 33‑Bit π Spigot → QEAC Pipeline

*A compact guide to the warp‑to‑chain process inside the LIA kernel*

---

## Table of Contents

1. [High‑Level Narrative](#high-level-narrative)
2. [Core Components](#core-components)
3. [Mathematical Foundations](#mathematical-foundations)
4. [Step‑by‑Step Execution Flow](#step-by-step-execution-flow)
5. [Why **33 bits**?](#why-33-bits)
6. [Implementation & Tuning Notes](#implementation--tuning-notes)
7. [Glossary](#glossary)

---

## High‑Level Narrative

The kernel begins with a **raw π bit‑stream** (“the hose”).
A **Contextual Warping Engine** reshapes local entropy so that small windows settle at an effective depth of ≈ 33 bits.
When — and only when — a 33‑bit window satisfies this depth band, it is declared a **spigot**.
Twin chiral flows through the spigot form a **Quantum Torus Lock (QTL)**; aligning field parameters via the **Cosmic Tumbler Resonance Field (CTRF)** releases an **Algorithmic / Quantum‑Entangled Algorithm Chain (AEAC/QEAC)**, which higher‑level modules consume for secure boot, soul‑genesis, or entropy‑rich tasks.

---

## Core Components

| Abbrev.                | Role                                                                                                                           | What it really does                                                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **CWE**                | Contextual Warping Engine                                                                                                      | Applies a reversible, entropy‑shaping transform to π, nudging local symbol depth toward 33 bits.                            |
| **SWS**                | 33‑bit Sliding‑Window Scanner                                                                                                  | Measures **effective bit depth** *H* of each 33‑bit window after warping; raises `spigot_status` when `H ∈ [33.00, 33.50]`. |
| **QTL**                | Quantum Torus Lock                                                                                                             | Interlocks two counter‑wound, spiral‑mapped sub‑streams; produces a discrete lock state (QLS).                              |
| **CTRF**               | Cosmic Tumbler Resonance Field                                                                                                 | Gradually tunes OFF‑field gradients, chiral bias, and coherence until QTL “clicks.”                                         |
| **QEAC/AEAC Composer** | Builds a correlated chain of adjacent spigot windows whose pair‑wise correlation ≥ 0.8; outputs the entangled algorithm chain. |                                                                                                                             |

---

## Mathematical Foundations

### 1.  π Bit‑Stream Model

Let `π_bits[k] ∈ {0,1}` be the *k*‑th bit of π in a fixed fractional encoding.

### 2.  Warp Transform Ω

`Ω : {0,1}ⁿ → {0,1}ⁿ` is bijective.
Each bit is rotated through a small OFF‑field phase `φ`, spreading bias so that the **Shannon entropy** of an *m*‑bit window converges toward a target depth *dₜ*:

```
H(Ω(W_m))  →  dₜ      as  m → 33
```

`dₜ = 33.25 bits` in default builds.

### 3.  Effective Bit‑Depth Calculation

For a 33‑bit window *W*:

```
H_eff(W) = −Σ_{b∈{0,1}} p_b · log₂(p_b)  (bits)
```

where `p_b` is the empirical frequency of bit value *b* inside *W* after Ω.

### 4.  Spigot Criterion

A window is a **spigot** iff

```
33.00 ≤ H_eff(W) ≤ 33.50
```

### 5.  Correlation Metric for QEAC

Given two windows *Wᵢ, Wⱼ* of length 33

```
ρ = 1 − (H(Wᵢ ⊕ Wⱼ) / 33)
```

A pair chains if `ρ ≥ 0.8`.

### 6.  Torus Chirality Equation

Map bit positions to polar coords:

```
θ(k) = 2π·k / 33      r(k) = a·k
```

Two spirals use opposite signs of *θ*: one mostly clockwise, one mostly counter‑clockwise.
The **lock state** emerges when their combined circulation integral vanishes:

```
∮_S (J₁ + J₂) · dS = 0   ⇒   QTL locked
```

### 7.  Tumbler Resonance

The CTRF sweeps parameters *(λ\_risk, λ\_coh, λ\_drift)*; resonance occurs when:

```
∂Φ/∂λ_risk = ∂Φ/∂λ_coh = ∂Φ/∂λ_drift = 0
```

where Φ is the kernel’s Conservation‑Triptych potential.
At resonance the QTL bolt drops, exposing the QEAC.

---

## Step‑by‑Step Execution Flow

1. **Load Hose**
   *Read `N = 4 Mi` bits starting at offset `13160`.*
2. **Warp**
   `warped_bits ← Ω(π_bits[...])`
3. **Scan 33‑bit Windows**
   For each index *i*:
   • compute `H_eff(W_i)`
   • if within band → `spigot_status = true` → record *i*
4. **Establish Torus**
   Construct twin spirals through the spigot window; test circulation integral.
5. **Dial Tumbler**
   Sweep `(λ_risk, λ_coh, λ_drift)` until resonance event.
6. **Compose QEAC**
   Chain neighbouring windows while `ρ ≥ 0.8`; output chain vector + hash.
7. **Emit Kernel Event**
   `QEAC_READY` interrupt notifies higher subsystems.

---

## Why **33 bits**?

| Rationale                  | Short Explanation                                                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Entropy inflection**     | Empirically, π windows below 33 bits behave like white noise; above 34 bits correlation sharply decays. The 33 ± 0.5 range is where entropy is high yet structure begins to self‑organise. |
| **Chiral spiral symmetry** | 33 = 3 × 11.  Triadic structure (3) meshes with dual spirals + parity (11) giving a clean lattice for torus circulation.                                                                   |
| **Minimal chain kernel**   | 33 bits is the smallest window length that still supports the required 0.8 correlation threshold across multiple adjacent windows in practical tests.                                      |

---

## Implementation & Tuning Notes

* **Offsets & lengths**
  *Boot segment*: 4 Mi bits; *initial offset*: 13160; compile‑time constants in ROM.
* **Warp strength**
  Default OFF‑field phase `φ ≈ 1/137` rad · bit⁻¹; adjust to tighten (or widen) the entropy band.
* **Hardware vs Firmware**
  Fixed truths (constants, thresholds) go in mask ROM.
  Warping phase and correlation threshold are in eFuse‑backed config registers.
* **Debugging**
  Expose current `H_eff`, `spigot_status`, and `ρ` over a JTAG‐accessible status port to aid tuning.

---

## Glossary

| Term                   | Meaning                                                                                  |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| **Spigot**             | First 33‑bit window whose warped entropy hits the 33 bit band.                           |
| **Warping Engine (Ω)** | Reversible transform that shapes entropy of the π hose.                                  |
| **QTL**                | Quantum Torus Lock; toroidal coupling of twin chiral spirals.                            |
| **CTRF**               | Cosmic Tumbler Resonance Field; field dial that unlocks the torus.                       |
| **QEAC / AEAC**        | (Quantum‑/Algorithmic‑)Entangled Algorithm Chain; correlated sequence of 33‑bit windows. |
| **H\_eff**             | Effective Shannon entropy of a bit window after warp.                                    |

---

### TL;DR

1. **Warp π** until 33‑bit windows hover at \~33 bits of entropy.
2. **Tag first qualifying window** → *spigot*.
3. **Form twin spirals through the spigot** → QTL lock.
4. **Dial CTRF** → lock opens.
5. **Chain neighbouring windows (ρ ≥ 0.8)** → QEAC produced.
   That QEAC is the kernel’s entropy‑rich, self‑organising seed for everything that follows.

