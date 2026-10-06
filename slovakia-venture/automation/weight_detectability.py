#!/usr/bin/env python3
"""Can a checkweigher detect a missing or doubled component in a ration pack?

Answers the question "how do we stop operators forgetting or doubling items?"
quantitatively. Replace COMPONENTS with the real BOM once "Cost the Pack"
(01-critical-path) produces it, then re-run:

    python3 weight_detectability.py

Anything printed as weight-blind needs a control that is not weight — a kit
nest or scan-to-close. See 14-error-proofing-kitting.md.

Model: pack weight = sum of component weights. Each component has a fill
tolerance, so the pack has natural weight variation. A missing or doubled item
is detectable only if its weight exceeds that noise by a workable margin.
"""
import math

# Representative 24h / 3600 kcal pack (R) — weights in grams.
COMPONENTS = [
    ("Retort main meal 1",      300),
    ("Retort main meal 2",      300),
    ("Crispbread / rusks",      125),
    ("Biscuit / energy bar",     60),
    ("Pate / spread tin",        75),
    ("Cheese spread sachet",     30),
    ("Jam sachet",               25),
    ("Honey sachet",             20),
    ("Instant coffee sachet",     2),
    ("Tea bag",                   2),
    ("Sugar sachets",             8),
    ("Isotonic drink powder",    35),
    ("Chocolate bar",            50),
    ("Chewing gum",               3),
    ("Salt / pepper sachet",      1),
    ("Water purification tabs",   5),
    ("Spoon",                     4),
    ("Wet wipe",                  6),
    ("Matches",                   5),
    ("Flameless heater",         35),
]
TOL_PCT = 3.0          # +/- 3% fill tolerance per component, treated as 3 sigma
SCALE_SD = 0.5         # checkweigher repeatability, grams

total = sum(w for _, w in COMPONENTS)
comp_sd = [(w * TOL_PCT / 100) / 3 for _, w in COMPONENTS]
pack_sd = math.sqrt(sum(sd * sd for sd in comp_sd) + SCALE_SD ** 2)

print(f"Pack nominal weight      : {total:,} g")
print(f"Components               : {len(COMPONENTS)}")
print(f"Pack weight 1 sigma      : {pack_sd:.2f} g   (component fill tolerance + scale)")
print(f"Practical reject window  : +/- {3*pack_sd:.1f} g  (3 sigma)")
print()
print(f"{'COMPONENT':<26}{'g':>5}{'sigmas':>9}  DETECTABLE IF MISSING/DOUBLED?")
print("-" * 78)
detect, marginal, blind = [], [], []
for name, w in sorted(COMPONENTS, key=lambda c: -c[1]):
    sigmas = w / pack_sd
    if sigmas >= 6:
        verdict, bucket = "YES - unambiguous", detect
    elif sigmas >= 3:
        verdict, bucket = "marginal - will miss some", marginal
    else:
        verdict, bucket = "NO - inside noise", blind
    bucket.append(name)
    print(f"{name:<26}{w:>5}{sigmas:>9.1f}  {verdict}")

print("-" * 78)
print(f"Weight-detectable (>=6 sigma): {len(detect)}/{len(COMPONENTS)} components")
print(f"Marginal (3-6 sigma)         : {len(marginal)}/{len(COMPONENTS)}")
print(f"BLIND to weight (<3 sigma)   : {len(blind)}/{len(COMPONENTS)}")
print()
blind_mass = sum(w for n, w in COMPONENTS if n in blind)
print(f"The {len(blind)} weight-blind components are {blind_mass} g = "
      f"{100*blind_mass/total:.1f}% of pack mass")
print()
# Cancelling-error case
print("CANCELLING ERROR: one item doubled, another omitted")
for a, b in [("Jam sachet", "Honey sachet"), ("Chocolate bar", "Isotonic drink powder")]:
    wa = dict(COMPONENTS)[a]; wb = dict(COMPONENTS)[b]
    net = abs(wa - wb)
    print(f"  +1 {a} ({wa} g) / -1 {b} ({wb} g)  -> net {net} g = "
          f"{net/pack_sd:.1f} sigma  {'DETECTED' if net/pack_sd>=3 else 'INVISIBLE to weight'}")
