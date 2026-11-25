"""CPR Lifeline prototype rig (scotch-yoke compression tester), units: mm.

Spec taken from the video narration:
  - DC motor, 150 W, 3000 RPM
  - double-stage spur gear reducer, 25:1  -> 120 RPM out (5:1 x 5:1)
  - scotch yoke, sliding pin at radius 25 mm -> linear rod stroke 50 mm (~2 in)
  - linear rod end: 80 mm dia x 15 mm microfiber pad
  - wooden table-style frame, parts otherwise 3D printed
Axes: Z up, rod along Z, gear shafts along Y.
"""
import math
import cadquery as cq

# ---------- parameters ----------
MODULE = 1.5
Z_PIN, Z_GEAR = 16, 80                      # 5:1 per stage
R_PIN, R_GEAR = MODULE * Z_PIN / 2, MODULE * Z_GEAR / 2
CD = R_PIN + R_GEAR                         # centre distance = 72
CRANK_R = 25.0                              # scotch-yoke pin radius
SHAFT_Z = 400.0                             # height of gear axes
PLATE_TOP = 319.0

def gear(zt, thick, bore, x, y0, z):
    """Spur gear, axis along +Y, spanning y0..y0+thick, centred at (x, z).
    Tooth centred on +X axis for phase control is applied by caller via rotate."""
    ra = MODULE * (zt + 2) / 2
    rr = MODULE * (zt - 2.5) / 2
    rp = MODULE * zt / 2
    pitch = 2 * math.pi / zt
    pts = []
    for i in range(zt):
        a = i * pitch
        for da, r in ((-0.30, rr), (-0.17, ra), (0.17, ra), (0.30, rr)):
            pts.append((r * math.cos(a + da * pitch * 1.6),
                        r * math.sin(a + da * pitch * 1.6)))
    w = (cq.Workplane("XZ", origin=(0, y0, 0)).polyline(pts).close()
         .extrude(-thick))
    w = w.cut(cq.Workplane("XZ", origin=(0, y0 - 1, 0)).circle(bore / 2).extrude(-thick - 2))
    return w, pitch

def place(w, x, z, phase_deg=0.0):
    # rotate about the Y axis through origin (phase), then move to (x, z)
    return (w.rotate((0, 0, 0), (0, 1, 0), -phase_deg)).translate((x, 0, z))

# ---------- frame (wood) ----------
LEG, W, D = 38.0, 400.0, 300.0
frame = cq.Workplane("XY").box(W, D, 19, centered=(True, True, False))               # base board
for sx in (-1, 1):
    for sy in (-1, 1):
        frame = frame.union(
            cq.Workplane("XY").box(LEG, LEG, 300 - 19, centered=(True, True, False))
            .translate((sx * (W / 2 - LEG / 2), sy * (D / 2 - LEG / 2), 19)))
top = (cq.Workplane("XY").box(W, D, 19, centered=(True, True, False)).translate((0, 0, 300))
       .cut(cq.Workplane("XY").circle(13).extrude(40).translate((0, 22, 290))))
# support board for the gear train
support = (cq.Workplane("XY").box(270, 12, 480 - PLATE_TOP, centered=(False, False, False))
           .translate((-80, -40, PLATE_TOP)))
for (hx, hz, hd) in ((0, SHAFT_Z, 22), (CD, SHAFT_Z, 22), (2 * CD, SHAFT_Z, 22)):
    support = support.cut(cq.Workplane("XZ", origin=(hx, -20, hz)).circle(hd / 2).extrude(30))
wood = frame.union(top).union(support)

# ---------- motor ----------
motor_x = 2 * CD
motor = (cq.Workplane("XZ", origin=(motor_x, -40, SHAFT_Z)).circle(30).extrude(100))   # body y -40..-140
motor = motor.union(cq.Workplane("XZ", origin=(motor_x, -140, SHAFT_Z)).circle(14).extrude(8))
motor_shaft = cq.Workplane("XZ", origin=(motor_x, -40, SHAFT_Z)).circle(4).extrude(-30)             # y -40..-10

# ---------- gears ----------
# plane 1: motor pinion -> intermediate big gear      y -24..-14
# plane 2: intermediate pinion -> output big gear     y  -8..  2
g_pin1, p16 = gear(Z_PIN, 10, 8, 0, -24, 0)
g_big1, p80 = gear(Z_GEAR, 10, 8, 0, -24, 0)
g_pin2, _ = gear(Z_PIN, 10, 8, 0, -8, 0)
g_big2, _ = gear(Z_GEAR, 10, 12, 0, -8, 0)
deg16, deg80 = math.degrees(p16), math.degrees(p80)
motor_pinion = place(g_pin1, motor_x, SHAFT_Z, 0)                       # tooth at +X ... mesh toward -X
inter_big = place(g_big1, CD, SHAFT_Z, 180 + 0 - 180 + deg80 / 2 * 0)    # gap/tooth phase tuned below
inter_big = place(g_big1, CD, SHAFT_Z, 0.5 * deg80 + 0.0)
inter_pin = place(g_pin2, CD, SHAFT_Z, 0)
out_big = place(g_big2, 0, SHAFT_Z, 0.5 * deg80)

# ---------- shafts ----------
inter_shaft = cq.Workplane("XZ", origin=(CD, -40, SHAFT_Z)).circle(4).extrude(-45)        # y -40..5
crank_shaft = cq.Workplane("XZ", origin=(0, -40, SHAFT_Z)).circle(6).extrude(-54)         # y -40..14

# ---------- crank disc + pin ----------
crank = (cq.Workplane("XZ", origin=(0, 6, SHAFT_Z)).circle(35).extrude(-8)
         .union(cq.Workplane("XZ", origin=(CRANK_R, 14, SHAFT_Z)).circle(4.5).extrude(-16)))
crank = crank.cut(cq.Workplane("XZ", origin=(0, 5, SHAFT_Z)).circle(6).extrude(-10))

# ---------- yoke + linear rod ----------
YOKE_Y0, YOKE_T = 16.0, 12.0
yoke = (cq.Workplane("XZ", origin=(0, YOKE_Y0, SHAFT_Z)).rect(110, 90).extrude(-YOKE_T))
slot = (cq.Workplane("XZ", origin=(0, YOKE_Y0 - 1, SHAFT_Z)).slot2D(2 * CRANK_R + 10, 10).extrude(-YOKE_T - 2))
yoke = yoke.cut(slot)
rod = (cq.Workplane("XY", origin=(0, YOKE_Y0 + YOKE_T / 2, 150)).circle(10).extrude(SHAFT_Z - 45 - 150 + 2))
rod_yoke = yoke.union(rod)

# ---------- guide bushing under top plate ----------
bushing = (cq.Workplane("XY", origin=(0, 22, 262)).circle(20).extrude(38)
           .cut(cq.Workplane("XY", origin=(0, 22, 260)).circle(10.2).extrude(45)))

# ---------- pad ----------
holder = cq.Workplane("XY", origin=(0, 22, 145)).circle(40).extrude(5)
pad = (cq.Workplane("XY", origin=(0, 22, 130)).circle(40).extrude(15))

# ---------- assemble ----------
asm = cq.Assembly(name="CPR_Lifeline_Test_Rig")
def add(name, shape, color):
    asm.add(shape, name=name, color=cq.Color(*color))

add("wood_frame", wood, (0.80, 0.62, 0.38))
add("motor_150W", motor, (0.12, 0.12, 0.12))
add("motor_shaft", motor_shaft, (0.7, 0.7, 0.72))
add("motor_pinion_z16", motor_pinion, (0.1, 0.1, 0.1))
add("intermediate_gear_z80", inter_big, (0.1, 0.1, 0.1))
add("intermediate_pinion_z16", inter_pin, (0.1, 0.1, 0.1))
add("output_gear_z80", out_big, (0.1, 0.1, 0.1))
add("intermediate_shaft", inter_shaft, (0.7, 0.7, 0.72))
add("crank_shaft", crank_shaft, (0.7, 0.7, 0.72))
add("crank_disc_pin", crank, (0.1, 0.1, 0.1))
add("scotch_yoke_linear_rod", rod_yoke, (0.1, 0.1, 0.1))
add("guide_bushing", bushing, (0.15, 0.15, 0.15))
add("pad_holder", holder, (0.1, 0.1, 0.1))
add("microfiber_pad_80x15", pad, (0.93, 0.93, 0.93))

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "cpr_lifeline_rig.step"
    asm.save(out)
    # also single-part STEPs/STLs for individual import
    parts = {n: o for n, o in [
        ("wood_frame", wood), ("motor", motor), ("gear_z16", g_pin1), ("gear_z80", g_big1),
        ("crank_disc_pin", crank), ("yoke_rod", rod_yoke), ("pad", pad)]}
    for n, o in parts.items():
        cq.exporters.export(o, f"{n}.stl")
    bb = cq.Workplane("XY").add(wood).val().BoundingBox()
    print("ok", out, "frame bbox", bb.xlen, bb.ylen, bb.zlen)
