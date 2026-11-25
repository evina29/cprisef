# cprisef

cprisef is a proposal for a hands free cpr compression rig with ai guidance, for isef.

## the problem

when someone collapses, good chest compressions have to start right away and keep a steady pace. rescuers get tired within a couple of minutes, their depth and rhythm drift, and the person doing the compressions is often untrained and scared. i propose testing whether a machine can hold the pace so that people can focus on calling for help and guiding the rescue.

## the proposal

cprisef is a test rig that performs compressions by itself. a motor drives a two stage gearbox, and a scotch yoke turns the spinning motion into a straight up and down push. the pad presses about 50 mm at 120 compressions a minute with roughly 500 n of force.

an ai guidance layer will sit on top of the rig and tell the rescuer what to do next. its design is the next stage of the project.

## cad model

the model is written in python with cadquery and builds a step file that opens in onshape or any other cad tool.

    pip install -r requirements.txt
    python cprisef.py cprisef_rig.step

## screenshots

### full 3d assembly

![3d assembly](docs/assembly.svg)

### wiring diagram

![wiring diagram](docs/wiring.svg)

### pcb

there is no custom pcb. the motor runs from an off the shelf speed controller, so the wiring diagram is the full electrical design.

### 3d render

the assembly picture above is the render, and github actions also builds the step file on every push.

## specifications

| item | value |
|---|---|
| motor | 150 w dc, 3000 rpm, 12 v version |
| gearbox | two stage spur gears, 25 to 1 total |
| gear module | 1.5, with 16 tooth and 80 tooth gears |
| output speed | 120 compressions per minute |
| mechanism | scotch yoke, 25 mm crank radius |
| stroke | 50 mm |
| peak force | about 500 n |
| frame | wood |

## materials and links

everything below is sold on amazon, and each link goes to the listing with the current price. the 80 tooth gears are bored to match the 8 mm and 12 mm shafts before assembly.

### motion and drive

| part | what it is for | qty | link |
|---|---|---|---|
| 150 w permanent magnet dc motor, choose the 12 v option | this is the motor, and the listing says it spins at 3000 rpm on 12 v. | 1 | [amazon](https://www.amazon.com/Speed-Permanent-Magnet-Generator-3000RPM/dp/B07J4RBJ1G) |
| 16 tooth steel spur gear, module 1.5, 8 mm bore | these are the two pinions. | 2 | [amazon](https://www.amazon.com/16-tooth-metal-gear/s?k=16+tooth+metal+gear) |
| 80 tooth steel spur gear, module 1.5, step bore | these are the two big gears. | 2 | [amazon](https://www.amazon.com/clp/B07RN6F15V) |
| kp08 pillow block bearings, 8 mm bore, pack of 4 | these hold the 8 mm intermediate shaft. | 1 pack | [amazon](https://www.amazon.com/clp/B073LDH4L7) |
| kp001 pillow block bearings, 12 mm bore, pack of 4 | these hold the 12 mm output shaft. | 1 pack | [amazon](https://www.amazon.com/uxcell-Pillow-Bearings-Bearing-Mounted/dp/B0FCSDWNB1) |
| 8 mm x 300 mm hardened steel rod, pack of 2 | this is the intermediate shaft. | 1 pack | [amazon](https://www.amazon.com/Othmro-Hardened-Chrome-Plated-8mmx300mm/dp/B081YJ7Y8N) |
| 12 mm x 300 mm hardened steel rod, pack of 2 | this is the output shaft. | 1 pack | [amazon](https://www.amazon.com/Coavoo-Linear-Diameter-Hardened-Chrome/dp/B0CN2H35LZ) |
| metric screw, nut and washer kit, m4 to m6 | this covers the mounting hardware and the crank pin. | 1 | [amazon](https://www.amazon.com/Washers-Assortment-Metric-Stainless-Machine/dp/B0CCP4VWZN) |

### frame

| part | what it is for | qty | link |
|---|---|---|---|
| 3/4 inch birch plywood, 24 by 24 inch, pack of 3 | this is for the frame, the yoke and the pad. | 1 pack | [amazon](https://www.amazon.com/Custom-Size-Thick-Birch-Plywood/dp/B08XBQYK8S) |

### power and wiring

| part | what it is for | qty | link |
|---|---|---|---|
| 12 v 30 a 360 w switching power supply | this powers the motor. | 1 | [amazon](https://www.amazon.com/SUPERNIGHT-Switching-Universal-Regulated-Transformer/dp/B01LATMSGS) |
| 20 a pwm dc motor speed controller, 10 to 60 v | this sets the motor speed. | 1 | [amazon](https://www.amazon.com/Controller-Regulator-Governor-Stepless-Modulator/dp/B0789JPD2G) |
| 14 awg silicone wire, red and black, 20 ft each | this is the main wiring. | 1 | [amazon](https://www.amazon.com/BNTECHGO-Silicone-Flexible-Stranded-Copper/dp/B08Q43DNKB) |
| inline fuse holders with assorted blade fuses, including 20 a | this protects the motor circuit. | 1 pack | [amazon](https://www.amazon.com/VicVan-Pack-Inline-Fuse-Holder/dp/B0CLK77GYN) |
| 22 mm latching emergency stop button | this stops the rig quickly. | 1 | [amazon](https://www.amazon.com/Uxcell-a14122300ux0109-Emergency-Latching-Mushroo/dp/B00W947PS0) |
| heat shrink wire connector kit | these are the crimp and ring terminals. | 1 | [amazon](https://www.amazon.com/clp/B01LXTK37Y) |
| heat shrink tubing assortment | this insulates the soldered joints. | 1 | [amazon](https://www.amazon.com/Heat-Shrink-Tubing-Kit-Automotive/dp/B0BJ2FP35V) |
| 14 awg power cord with bare wire end, 6 ft | this brings mains power to the supply. | 1 | [amazon](https://www.amazon.com/14-awg-power-cord/s?k=14+awg+power+cord) |

### soldering and tools

| part | what it is for | qty | link |
|---|---|---|---|
| 80 w adjustable temperature soldering iron kit with stand, tips, flux, tweezers and desoldering pump | this is the soldering iron and its accessories. | 1 | [amazon](https://www.amazon.com/Soldering-Adjustable-Temperature-Electronics-Desoldering/dp/B0BW4HMXJ3) |
| 63/37 rosin core solder wire, 0.8 mm | this is extra solder for the joints. | 1 | [amazon](https://www.amazon.com/Twocorn-no-wash-tin-Lead-Electric-Soldering/dp/B0CP7QHFL6) |
| digital multimeter with wire stripper | this checks voltage and continuity and strips wire. | 1 | [amazon](https://www.amazon.com/KAIWEETS-Digital-Multimeter-Wire-Stripper/dp/B09NBZCNMG) |

### safety

| part | what it is for | qty | link |
|---|---|---|---|
| ansi z87.1 safety glasses | these protect eyes during building and testing. | 1 | [amazon](https://www.amazon.com/safety-glasses-z87-1/s?k=safety+glasses+z87.1) |

### testing and ai guidance

| part | what it is for | qty | link |
|---|---|---|---|
| adult cpr training manikin | tests are done on a manikin and never on a person. | 1 | [amazon](https://www.amazon.com/cpr-training-manikin/s?k=cpr+training+manikin) |
| load cell kit with hx711 amplifier | this measures the compression force. | 1 | [amazon](https://www.amazon.com/Bridge-Weighting-Sensor-Strain-Individual/dp/B0DHZXV8XR) |
| raspberry pi 5 starter kit | this runs the ai guidance software. | 1 | [amazon](https://www.amazon.com/Vilros-Raspberry-Starter-Kit-MAX/dp/B0D232HN74) |
| 5 mp camera module for raspberry pi | this lets the software watch the compressions. | 1 | [amazon](https://www.amazon.com/Arducam-Megapixels-Sensor-OV5647-Raspberry/dp/B012V1HEP4) |

## safety and ethics

no human participants are involved. the rig is only tested on a manikin or a force sensor, never on a person. the motor circuit has a fuse and an emergency stop, and the emergency stop must be rated for the motor current of about 12.5 a. wiring the power cord to the supply involves mains voltage and should only be done by someone who can do it safely.

cprisef is a science fair proposal and not a medical device, so it must never be used on a real patient. it follows the isef rules on safety, ethics, academic integrity and generative ai, and the design that inspired it is credited in the project paperwork.
