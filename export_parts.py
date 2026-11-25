"""Export every part of the cprisef assembly as its own STEP file (units: mm).

usage: python export_parts.py [output_folder]
"""
import os
import sys

import cadquery as cq

import cprisef

out = sys.argv[1] if len(sys.argv) > 1 else "step"
os.makedirs(out, exist_ok=True)
for child in cprisef.asm.children:
    shape = child.obj
    if isinstance(shape, cq.Workplane):
        shape = cq.Workplane("XY").add(shape.vals())
    path = os.path.join(out, f"{child.name}.step")
    cq.exporters.export(shape, path, opt={"write_pcurves": False})  # smaller files
    print("wrote", path, os.path.getsize(path), "bytes")
