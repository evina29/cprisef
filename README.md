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
