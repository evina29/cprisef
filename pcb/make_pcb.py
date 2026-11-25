"""Generate the cprisef interface board (kicad project files, gerbers and drill files).

The board is a small 70 x 70 mm two layer interface between a raspberry pi pico,
an hx711 load cell amplifier, an emergency stop sense input, a buzzer and a status led.
Run: python make_pcb.py   (writes into ./kicad and ./gerbers)
"""
import json
import os
import uuid
import zipfile

W = H = 70.0
PITCH = 2.54
PAD, DRILL, TRACK = 1.8, 1.0, 0.4
HERE = os.path.dirname(os.path.abspath(__file__))
KDIR, GDIR = os.path.join(HERE, "kicad"), os.path.join(HERE, "gerbers")
os.makedirs(KDIR, exist_ok=True)
os.makedirs(GDIR, exist_ok=True)

NETS = ["", "GND", "3V3", "UART_TX", "UART_RX", "HX_DT", "HX_SCK", "ESTOP", "BUZZER", "LED"]
NID = {n: i for i, n in enumerate(NETS)}


def uid():
    return str(uuid.uuid4())


# ---------------------------------------------------------------- parts
PICO_X, PICO_Y = 25.0, 8.0
RIGHT_DX = 17.78
pico_pins = {1: "UART_TX", 2: "UART_RX", 3: "GND", 8: "GND", 13: "GND", 18: "GND", 19: "LED",
             23: "GND", 24: "BUZZER", 28: "GND", 29: "ESTOP", 31: "HX_SCK", 32: "HX_DT",
             33: "GND", 36: "3V3", 38: "GND"}
pico_names = {1: "GP0", 2: "GP1", 3: "GND", 4: "GP2", 5: "GP3", 6: "GP4", 7: "GP5", 8: "GND",
              9: "GP6", 10: "GP7", 11: "GP8", 12: "GP9", 13: "GND", 14: "GP10", 15: "GP11",
              16: "GP12", 17: "GP13", 18: "GND", 19: "GP14", 20: "GP15", 21: "GP16", 22: "GP17",
              23: "GND", 24: "GP18", 25: "GP19", 26: "GP20", 27: "GP21", 28: "GND", 29: "GP22",
              30: "RUN", 31: "GP26", 32: "GP27", 33: "GND", 34: "GP28", 35: "ADC_VREF",
              36: "3V3", 37: "3V3_EN", 38: "GND", 39: "VSYS", 40: "VBUS"}


def pico_pad(n):
    if n <= 20:
        return (0.0, (n - 1) * PITCH)
    return (RIGHT_DX, (40 - n) * PITCH)


def row_y(r):
    return PICO_Y + r * PITCH


# (ref, value, footprint, x, y, [(pin, net, dx, dy)], silk rectangle (x0,y0,x1,y1) relative)
parts = []
pads_pico = [(str(n), pico_pins.get(n, ""), *pico_pad(n)) for n in range(1, 41)]
parts.append(("U1", "Raspberry_Pi_Pico", "cprisef:RPi_Pico_THT", PICO_X, PICO_Y, pads_pico,
              (-1.6, -2.0, RIGHT_DX + 1.6, 19 * PITCH + 2.0)))


def header(ref, value, x, rows_nets):
    """vertical 1xN header, pin 1 at the first row; rows_nets is a list of (row, net)."""
    y0 = row_y(rows_nets[0][0])
    pads = [(str(i + 1), net, 0.0, row_y(r) - y0) for i, (r, net) in enumerate(rows_nets)]
    n = len(rows_nets)
    parts.append((ref, value, f"cprisef:Header_1x{n:02d}_P2.54mm", x, y0, pads,
                  (-1.27, -1.27, 1.27, (n - 1) * PITCH + 1.27)))


header("J1", "UART_to_pi", 10.0, [(0, "UART_TX"), (1, "UART_RX"), (2, "GND")])
header("J2", "HX711_module", 55.0, [(6, "3V3"), (7, "GND"), (8, "HX_DT"), (9, "HX_SCK")])
header("J3", "ESTOP_input", 55.0, [(11, "ESTOP"), (12, "GND")])
header("J4", "BUZZER", 55.0, [(16, "BUZZER"), (17, "GND")])
header("J5", "STATUS_LED", 10.0, [(17, "GND"), (18, "LED")])
parts.append(("C1", "100nF", "cprisef:C_Disc_P2.54mm", 51.0, row_y(6),
              [("1", "3V3", 0.0, 0.0), ("2", "GND", 0.0, PITCH)], (-1.27, -1.27, 1.27, PITCH + 1.27)))

MOUNT = [(4.0, 4.0), (66.0, 4.0), (4.0, 66.0), (66.0, 66.0)]
MOUNT_D = 3.2

# top layer tracks: (net, [points]); every ground pad connects through the bottom ground pour
tracks = [
    ("UART_TX", [(PICO_X, row_y(0)), (10.0, row_y(0))]),
    ("UART_RX", [(PICO_X, row_y(1)), (10.0, row_y(1))]),
    ("LED", [(PICO_X, row_y(18)), (10.0, row_y(18))]),
    ("3V3", [(PICO_X + RIGHT_DX, row_y(4)), (48.0, row_y(4)), (48.0, row_y(6)), (55.0, row_y(6))]),
    ("HX_DT", [(PICO_X + RIGHT_DX, row_y(8)), (55.0, row_y(8))]),
    ("HX_SCK", [(PICO_X + RIGHT_DX, row_y(9)), (55.0, row_y(9))]),
    ("ESTOP", [(PICO_X + RIGHT_DX, row_y(11)), (55.0, row_y(11))]),
    ("BUZZER", [(PICO_X + RIGHT_DX, row_y(16)), (55.0, row_y(16))]),
]


def abs_pads():
    out = []
    for ref, val, fp, x, y, pads, _ in parts:
        for num, net, dx, dy in pads:
            out.append((ref, num, net, x + dx, y + dy))
    return out


# ---------------------------------------------------------------- kicad pcb
def kicad_pcb():
    s = ['(kicad_pcb (version 20221018) (generator cprisef_make_pcb)',
         ' (general (thickness 1.6))', ' (paper "A4")', ' (layers',
         '  (0 "F.Cu" signal) (31 "B.Cu" signal) (32 "B.Adhes" user "B.Adhesive")',
         '  (33 "F.Adhes" user "F.Adhesive") (34 "B.Paste" user) (35 "F.Paste" user)',
         '  (36 "B.SilkS" user "B.Silkscreen") (37 "F.SilkS" user "F.Silkscreen")',
         '  (38 "B.Mask" user) (39 "F.Mask" user) (44 "Edge.Cuts" user)',
         '  (46 "B.CrtYd" user "B.Courtyard") (47 "F.CrtYd" user "F.Courtyard")',
         '  (48 "B.Fab" user) (49 "F.Fab" user))',
         ' (setup (pad_to_mask_clearance 0.05) (pcbplotparams (layerselection 0x00010fc_ffffffff)',
         '  (outputformat 1) (outputdirectory "../gerbers/")))']
    for i, n in enumerate(NETS):
        s.append(f' (net {i} "{n}")')
    for ref, val, fp, x, y, pads, sil in parts:
        s.append(f' (footprint "{fp}" (layer "F.Cu") (tstamp {uid()}) (at {x:.3f} {y:.3f})')
        s.append('  (attr through_hole)')
        s.append(f'  (fp_text reference "{ref}" (at 0 -3) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))) (tstamp {uid()}))')
        s.append(f'  (fp_text value "{val}" (at 0 -4.5) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))) (tstamp {uid()}))')
        x0, y0, x1, y1 = sil
        for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
            s.append(f'  (fp_line (start {a[0]:.3f} {a[1]:.3f}) (end {b[0]:.3f} {b[1]:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS") (tstamp {uid()}))')
        for num, net, dx, dy in pads:
            shape = "rect" if num == "1" else "circle"
            netp = f' (net {NID[net]} "{net}")' if net else ""
            s.append(f'  (pad "{num}" thru_hole {shape} (at {dx:.3f} {dy:.3f}) (size {PAD} {PAD}) (drill {DRILL}) (layers "*.Cu" "*.Mask"){netp} (tstamp {uid()}))')
        s.append(' )')
    for i, (mx, my) in enumerate(MOUNT):
        s.append(f' (footprint "cprisef:MountingHole_3.2mm" (layer "F.Cu") (tstamp {uid()}) (at {mx} {my})')
        s.append('  (attr exclude_from_pos_files exclude_from_bom)')
        s.append(f'  (fp_text reference "H{i + 1}" (at 0 -3) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))) (tstamp {uid()}))')
        s.append(f'  (fp_text value "MountingHole" (at 0 3) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))) (tstamp {uid()}))')
        s.append(f'  (pad "" np_thru_hole circle (at 0 0) (size {MOUNT_D} {MOUNT_D}) (drill {MOUNT_D}) (layers "*.Cu" "*.Mask") (tstamp {uid()}))')
        s.append(' )')
    for net, pts in tracks:
        for a, b in zip(pts, pts[1:]):
            s.append(f' (segment (start {a[0]:.3f} {a[1]:.3f}) (end {b[0]:.3f} {b[1]:.3f}) (width {TRACK}) (layer "F.Cu") (net {NID[net]}) (tstamp {uid()}))')
    for a, b in (((0, 0), (W, 0)), ((W, 0), (W, H)), ((W, H), (0, H)), ((0, H), (0, 0))):
        s.append(f' (gr_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (stroke (width 0.1) (type solid)) (layer "Edge.Cuts") (tstamp {uid()}))')
    s.append(f' (zone (net 1) (net_name "GND") (layer "B.Cu") (tstamp {uid()}) (hatch edge 0.5)')
    s.append('  (connect_pads (clearance 0.3)) (min_thickness 0.25) (filled_areas_thickness no)')
    s.append('  (fill yes (thermal_gap 0.5) (thermal_bridge_width 0.5))')
    s.append(f'  (polygon (pts (xy 0.5 0.5) (xy {W - 0.5} 0.5) (xy {W - 0.5} {H - 0.5}) (xy 0.5 {H - 0.5}))))')
    s.append(')')
    return "\n".join(s) + "\n"


# ---------------------------------------------------------------- kicad schematic
def lib_symbol(name, left, right, ref_prefix="J"):
    """box symbol; left and right are lists of (number, pin name); pins passive."""
    rows = max(len(left), len(right))
    top = rows * 1.27
    out = [f'  (symbol "cprisef:{name}" (in_bom yes) (on_board yes)',
           f'   (property "Reference" "{ref_prefix}" (at 0 {top + 2.54:.2f} 0) (effects (font (size 1.27 1.27))))',
           f'   (property "Value" "{name}" (at 0 {-top - 2.54:.2f} 0) (effects (font (size 1.27 1.27))))',
           '   (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
           f'   (symbol "{name}_0_1" (rectangle (start -5.08 {top:.2f}) (end 5.08 {-top:.2f}) (stroke (width 0.254) (type default)) (fill (type background))))',
           f'   (symbol "{name}_1_1"']
    for i, (num, pname) in enumerate(left):
        out.append(f'    (pin passive line (at -7.62 {top - 1.27 - i * 2.54:.2f} 0) (length 2.54) (name "{pname}" (effects (font (size 1.0 1.0)))) (number "{num}" (effects (font (size 1.0 1.0)))))')
    for i, (num, pname) in enumerate(right):
        out.append(f'    (pin passive line (at 7.62 {top - 1.27 - i * 2.54:.2f} 180) (length 2.54) (name "{pname}" (effects (font (size 1.0 1.0)))) (number "{num}" (effects (font (size 1.0 1.0)))))')
    out.append('   ))')
    return "\n".join(out)


def kicad_sch():
    libs, inst, labels = [], [], []
    place = []  # (ref, value, fp, libname, left, right, nets{num: net}, x, y)
    pl = [(str(n), pico_names[n]) for n in range(1, 21)]
    pr = [(str(40 - r), pico_names[40 - r]) for r in range(20)]
    place.append(("U1", "Raspberry_Pi_Pico", "cprisef:RPi_Pico_THT", "RPi_Pico", pl, pr, {str(k): v for k, v in pico_pins.items()}, 140.0, 100.0))
    x = 40.0
    y = 40.0
    for ref, val, fp, x_, y_, pads, _ in parts[1:]:
        if ref == "C1":
            lname, left, right = "C", [("1", "1")], [("2", "2")]
        else:
            n = len(pads)
            lname, left, right = f"Conn_01x{n:02d}", [(p[0], f"Pin_{p[0]}") for p in pads], []
        nets = {p[0]: p[1] for p in pads}
        place.append((ref, val, fp, lname, left, right, nets, x, y))
        y += 35.0
        if y > 160:
            x, y = 240.0, 40.0
    done = set()
    for ref, val, fp, lname, left, right, nets, x, y in place:
        if lname not in done:
            libs.append(lib_symbol(lname, left, right, ref[0]))
            done.add(lname)
        rows = max(len(left), len(right))
        top = rows * 1.27
        inst.append(f'  (symbol (lib_id "cprisef:{lname}") (at {x:.2f} {y:.2f} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {uid()})')
        inst.append(f'   (property "Reference" "{ref}" (at {x:.2f} {y - top - 2.54:.2f} 0) (effects (font (size 1.27 1.27))))')
        inst.append(f'   (property "Value" "{val}" (at {x:.2f} {y + top + 2.54:.2f} 0) (effects (font (size 1.27 1.27))))')
        inst.append(f'   (property "Footprint" "{fp}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) hide))')
        for num, _ in left + right:
            inst.append(f'   (pin "{num}" (uuid {uid()}))')
        inst.append('  )')
        for side, pins, px in (("l", left, -7.62), ("r", right, 7.62)):
            for i, (num, _) in enumerate(pins):
                net = nets.get(num, "")
                if not net:
                    continue
                py = top - 1.27 - i * 2.54
                ang = 0 if side == "l" else 180
                labels.append(f'  (label "{net}" (at {x + px:.2f} {y - py:.2f} {ang}) (effects (font (size 1.27 1.27)) (justify {"right" if side == "l" else "left"} bottom)) (uuid {uid()}))')
    out = ['(kicad_sch (version 20230121) (generator cprisef_make_pcb)', f' (uuid {uid()})', ' (paper "A3")',
           ' (lib_symbols', *libs, ' )', *inst, *labels,
           ' (sheet_instances (path "/" (page "1")))', ')']
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- gerber / drill
def gflash_hdr(title, apertures):
    s = ["G04 cprisef make_pcb*", f"G04 {title}*", "%FSLAX46Y46*%", "%MOMM*%", "%LPD*%"]
    for code, d in apertures:
        s.append(f"%ADD{code}C,{d:.6f}*%")
    return s


def c(v):
    return f"{int(round(v * 1e6)):d}"


def gxy(x, y):
    return f"X{c(x)}Y{c(H - y)}"


def flash(code, x, y):
    return [f"D{code}*", f"{gxy(x, y)}D03*"]


def seg(code, a, b):
    return [f"D{code}*", f"{gxy(*a)}D02*", f"{gxy(*b)}D01*"]


def write(name, lines):
    with open(os.path.join(GDIR, name), "w") as f:
        f.write("\n".join(lines + ["M02*"]) + "\n")


def make_gerbers():
    P = abs_pads()
    hdr = gflash_hdr
    # top copper
    l = hdr("top copper", [(10, PAD), (11, TRACK)]) + ["G01*"]
    for _, _, _, x, y in P:
        l += flash(10, x, y)
    for net, pts in tracks:
        for a, b in zip(pts, pts[1:]):
            l += seg(11, a, b)
    write("cprisef-F_Cu.gtl", l)
    # bottom copper with ground pour and clearances around other nets
    l = hdr("bottom copper", [(10, PAD), (15, PAD + 0.6), (17, MOUNT_D + 0.6)]) + ["G01*", "D10*"]
    x0, y0, x1, y1 = 0.5, 0.5, W - 0.5, H - 0.5
    l += ["G36*", f"{gxy(x0, y0)}D02*", f"{gxy(x1, y0)}D01*", f"{gxy(x1, y1)}D01*", f"{gxy(x0, y1)}D01*", f"{gxy(x0, y0)}D01*", "G37*"]
    l += ["%LPC*%"]
    for _, _, net, x, y in P:
        if net != "GND":
            l += flash(15, x, y)
    for mx, my in MOUNT:
        l += flash(17, mx, my)
    l += ["%LPD*%"]
    write("cprisef-B_Cu.gbl", l)
    # solder mask openings
    for name, side in (("cprisef-F_Mask.gts", "top"), ("cprisef-B_Mask.gbs", "bottom")):
        l = hdr(f"{side} mask", [(12, PAD + 0.1)]) + ["G01*"]
        for _, _, _, x, y in P:
            l += flash(12, x, y)
        write(name, l)
    # top silkscreen outlines
    l = hdr("top silk", [(13, 0.15)]) + ["G01*"]
    for ref, val, fp, x, y, pads, (a0, b0, a1, b1) in parts:
        pts = [(x + a0, y + b0), (x + a1, y + b0), (x + a1, y + b1), (x + a0, y + b1), (x + a0, y + b0)]
        for a, b in zip(pts, pts[1:]):
            l += seg(13, a, b)
    write("cprisef-F_Silkscreen.gto", l)
    # board outline
    l = hdr("board outline", [(14, 0.1)]) + ["G01*"]
    pts = [(0, 0), (W, 0), (W, H), (0, H), (0, 0)]
    for a, b in zip(pts, pts[1:]):
        l += seg(14, a, b)
    write("cprisef-Edge_Cuts.gm1", l)
    # drill files
    def drl(name, d, pts):
        lines = ["M48", "; cprisef make_pcb", "FMAT,2", "METRIC", f"T1C{d:.3f}", "%", "G90", "G05", "T1"]
        lines += [f"X{x:.3f}Y{H - y:.3f}" for x, y in pts]
        lines += ["M30"]
        with open(os.path.join(GDIR, name), "w") as f:
            f.write("\n".join(lines) + "\n")
    drl("cprisef-PTH.drl", DRILL, [(x, y) for _, _, _, x, y in P])
    drl("cprisef-NPTH.drl", MOUNT_D, MOUNT)
    with zipfile.ZipFile(os.path.join(GDIR, "gerbers.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(GDIR)):
            if fn != "gerbers.zip":
                z.write(os.path.join(GDIR, fn), fn)


def main():
    open(os.path.join(KDIR, "cprisef.kicad_pcb"), "w").write(kicad_pcb())
    open(os.path.join(KDIR, "cprisef.kicad_sch"), "w").write(kicad_sch())
    open(os.path.join(KDIR, "cprisef.kicad_pro"), "w").write(json.dumps(
        {"meta": {"filename": "cprisef.kicad_pro", "version": 1}, "board": {}, "net_settings": {"classes": [{"name": "Default", "track_width": TRACK, "clearance": 0.2}]}, "sheets": [["", ""]]}, indent=2) + "\n")
    open(os.path.join(KDIR, "cprisef.kicad_prl"), "w").write(json.dumps(
        {"meta": {"filename": "cprisef.kicad_prl", "version": 3}, "board": {"active_layer": 0, "visible_layers": "0x00010fc_ffffffff"}, "project": {"files": []}}, indent=2) + "\n")
    make_gerbers()
    print("wrote kicad and gerber files")


if __name__ == "__main__":
    main()
