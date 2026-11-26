# CPRISEF

Hi! CPRISEF is a hands-free CPR compression rig with AI guidance. I am designing it for ISEF and building it for Fallen at Hack Club, and this repo has everything for the design: the CAD, the circuit board, the firmware and the parts list.

## Why I made it

When someone collapses, good chest compressions have to start right away and stay at a steady pace. But rescuers get tired in about two minutes, their depth and rhythm drift, and most people doing CPR have never practiced. I wanted to see if a machine could hold the pace so the people around can call for help and focus on the rescue. Then I wanted to add an AI layer on top that tells the rescuer what to do next. I am doing this because it felt like a hardware problem that actually matters.

## What it does

A 150 W motor drives a two-stage gearbox, and a scotch yoke turns the spinning into a straight up-and-down push. The pad presses about 50 mm at 120 compressions a minute with around 500 N of force. A load cell measures every push, and a Raspberry Pi Pico counts compressions, checks the rate, and beeps if it leaves the 100 to 120 per minute window or the emergency stop is hit. A Raspberry Pi 5 with a camera will run the AI guidance software, which is the next stage of the project.

It only ever gets tested on a manikin or a force sensor, never on a person.

## How to use this repo

The whole rig is written in Python with CadQuery, so you can rebuild the CAD yourself.

    pip install -r requirements.txt
    python cprisef.py cprisef_rig.step
    python export_parts.py step

The first command writes the full assembly as a STEP file that opens in Onshape or any other CAD tool. The second writes one STEP file per part. Both outputs are already in the repo too.

## Files in this repo

| Path | What it is |
|---|---|
| cprisef.py | Parametric CAD source for the whole rig |
| cprisef_rig.step | The full assembly as one STEP file |
| step/ | One STEP file for each of the 14 parts |
| export_parts.py | Writes the per-part STEP files |
| pcb/kicad/ | KiCad project, schematic and board for the interface board |
| pcb/gerbers/ | Gerbers, drill files and gerbers.zip for fabrication |
| pcb/make_pcb.py | Script that generates the KiCad files and gerbers |
| firmware/main.py | MicroPython firmware for the interface board |
| bom.csv | Bill of materials with a link, a price estimate and an owned note for every item |
| docs/ | The pictures used below |

## Screenshots

### Full 3D assembly

![3D assembly](docs/assembly.svg)

### Wiring diagram

![Wiring diagram](docs/wiring.svg)

### PCB

![PCB layout](docs/pcb.svg)

The interface board is a 70 by 70 mm two-layer board. It connects the Pico to the HX711 load cell amplifier, the emergency stop sense input, a buzzer, a status LED and a UART link to the Raspberry Pi. It carries no motor current, because the motor runs from the off-the-shelf speed controller. The schematic is in pcb/kicad/cprisef.kicad_sch.

Heads up: I generated the KiCad files and gerbers with pcb/make_pcb.py and have not ordered boards yet, so I will double-check the design rules before fabricating anything.

### Firmware

firmware/main.py runs on the Pico. It reads the load cell, counts compressions and their rate, sounds the buzzer when the rate is off or the emergency stop is pressed, and sends the rate to the Raspberry Pi once a second. It is written for this board and has not run on real hardware yet.

### 3D render

The assembly picture above is the render. The assembly source is cprisef.py, which is CadQuery instead of Fusion or FreeCAD, and the electronics source is the KiCad project in pcb/kicad.

## Specifications

| Item | Value |
|---|---|
| Motor | 150 W DC, 3000 rpm, 12 V version |
| Gearbox | Two-stage spur gears, 25 to 1 total |
| Gear module | 1.5, with 16-tooth and 80-tooth gears |
| Output speed | 120 compressions per minute |
| Mechanism | Scotch yoke, 25 mm crank radius |
| Stroke | 50 mm |
| Peak force | About 500 N |
| Frame | Wood |

## Parts and cost

Everything is from Amazon. bom.csv has a link for every item, and the estimated total is about $763 before tax and shipping. Those prices are my estimates, so I will check each one against its listing before ordering. bom.csv also says whether I already own each part, and right now I own none of them.

## Safety and ethics

No human participants are involved. The rig is only tested on a manikin or a force sensor, never on a person. The motor circuit has a fuse and an emergency stop, and the emergency stop must be rated for the motor current of about 12.5 A. Wiring the power cord to the supply involves mains voltage, so it should only be done by someone who can do it safely.

CPRISEF is a science fair project and not a medical device, so it must never be used on a real patient. It follows the ISEF rules on safety, ethics, academic integrity and generative AI, and the design that inspired it is credited in the project paperwork.
