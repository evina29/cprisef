# CPR Lifeline test rig (CAD)

A parametric CAD model (CadQuery, Python) of the scotch-yoke prototype rig built to validate the **CPR Lifeline**, an automatic, hands-free chest-compression device concept for cardiac arrest. The rig drives a padded rod at 120 compressions per minute with about 2 in (50 mm) of travel and about 500 N of force.

## What it is and how to use it

`cpr_rig.py` builds the whole rig as a 14-part assembly in millimetres and exports it as a STEP file, which opens in Onshape, Fusion, SolidWorks or FreeCAD.

```
pip install -r requirements.txt
python cpr_rig.py cpr_lifeline_rig.step
```

- Output: `cpr_lifeline_rig.step` plus one STL per main part.
- Onshape: **Create > Import**, then pick the STEP file.
- No local setup: run the **Build STEP** workflow in the Actions tab and download the `cpr-lifeline-rig-cad` artifact.
- Change sizes by editing the variables at the top of `cpr_rig.py` (gear module, tooth counts, crank radius, frame size, pad size) and rebuilding.

## Why I made it

Over 350,000 out-of-hospital cardiac arrests happen each year in the US and over 270,000 in the EU, and around 90% are fatal. A big reason is insufficient CPR, whether from bystanders or from delayed paramedics. A safe, automatic, hands-free CPR device would save time and effort and let medical teams focus on other care.

The current state of the art, the Lucas device, has drawbacks:

- It does not fit large patients, who have the highest likelihood of cardiac arrest.
- It causes more injuries (skin lesions, rib fractures) than manual CPR.
- It costs about $20,000 and is bulky, which hurts portability.

The CPR Lifeline addresses these with an adjustable padded strap that fits any chest size, full-contact microfiber pads (8 cm diameter, 1.5 cm thick) that spread pressure like a palm, a compact lightweight design with a bill of materials of about $200, and room for defibrillation pads to be placed diagonally so an AED can be used during CPR. This repo models the prototype test rig used to validate the mechanism.

## Screenshots

### Full 3D assembly

![3D assembly of the test rig, seen from the gear side](docs/assembly.svg)

Wood frame, 150 W motor, two-stage 25:1 gear train, scotch yoke, linear rod and microfiber pad. Gears are drawn as simple discs in this picture; the STEP file has toothed gears.

### Wiring diagram

![Wiring diagram: bench supply to DC motor](docs/wiring.svg)

### PCB

There is no PCB. The prototype runs the motor straight from a bench power supply, and the video shows no circuit board.

### 3D render

The assembly image above is the render. A render of the final strapped device is not part of this repo.

## Specs modelled

| Item | Value |
| --- | --- |
| Motor | 150 W DC, 3000 RPM |
| Reduction | two spur stages, 16T into 80T each, 25:1 total |
| Output speed | 120 RPM (120 compressions per minute) |
| Scotch-yoke crank radius | 25 mm (50 mm, about 2 in, of stroke) |
| Force target | about 500 N |
| Pad | 80 mm diameter, 15 mm thick microfiber |
| Frame | wooden table-style frame, other parts 3D printed |

Frame size, wood sizes, motor body size, gear widths and the gear tooth profile are estimates, not values from the source video.

## Future work

Medical-grade components and metal parts for durability, better microfiber pressure distribution, and a rechargeable lithium-polymer battery sized for about 30 minutes of use, which is longer than the average CPR duration.
# CPR Lifeline test rig (CAD)

Parametric CadQuery model of the scotch-yoke prototype rig from the CPR Lifeline project: an automatic chest-compression device concept (padded strap, 120 compressions/min, about 2 in depth, about 500 N).

## Specs modelled

| Item | Value |
| --- | --- |
| Motor | 150 W DC, 3000 RPM |
| Reduction | two spur stages, 16T into 80T each, 25:1 total |
| Output speed | 120 RPM (120 compressions/min) |
| Scotch-yoke crank radius | 25 mm (50 mm / about 2 in stroke) |
| Pad | 80 mm dia x 15 mm microfiber |
| Frame | wooden table-style frame, otherwise 3D-printed parts |

Frame size, wood sizes, motor body size, gear widths and the gear tooth profile are estimates and are not taken from the source video.

## Build the CAD files

```
pip install -r requirements.txt
python cpr_rig.py cpr_lifeline_rig.step
```

This writes `cpr_lifeline_rig.step` (14 named parts, millimetres) plus one STL per main part. Import the STEP into Onshape with **Create > Import**.

You can also run the **Build STEP** workflow in the Actions tab and download the `cpr-lifeline-rig-cad` artifact.

## Edit dimensions

All sizes are plain variables near the top of `cpr_rig.py` (module, tooth counts, crank radius, frame size, pad size). Change them and rebuild.
# cpr-lifeline-rig
Parametric CAD model (CadQuery) of the CPR Lifeline scotch-yoke test rig
