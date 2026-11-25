# cprisef

a hands free cpr compression rig with ai guidance, built for isef.

## the problem

when someone collapses, good chest compressions have to start right away and keep going at a steady pace. in real life that is hard. rescuers get tired within a couple of minutes, their depth and rhythm drift, and the person doing it is often untrained and scared. i wanted to see if a machine could hold the pace so a person can focus on calling for help and guiding the rescue.

## what we are building

cprisef is a test rig that does compressions by itself. a motor drives a two stage gearbox, and a scotch yoke turns the spinning motion into a straight up and down push. the pad presses about 50 mm at 120 compressions a minute with roughly 500 N of force.

the ai guidance part is still being defined. it will sit on top of this rig and tell the rescuer what to do next. (to be filled in by the team once the design is final.)

## how to use this repo

the cad model is written in python with cadquery. to build the step file:

    pip install -r requirements.txt
    python cprisef.py cprisef_rig.step

you can import the step file into onshape or any other cad tool. every push to main also builds it with github actions, and you can download the files from the actions tab.

## what is in this repo

| file | what it is |
|---|---|
| cprisef.py | parametric cad script for the whole rig |
| requirements.txt | python packages needed |
| .github/workflows/build-step.yml | builds the step and stl files on every push |
| docs/assembly.svg | full 3d assembly picture |
| docs/wiring.svg | wiring diagram |

## screenshots

### full 3d assembly

![3d assembly](docs/assembly.svg)

### wiring diagram

![wiring diagram](docs/wiring.svg)

### pcb

there is no custom pcb in this version. the motor runs from an off the shelf speed controller, so the wiring diagram above is the full electrical design.

### 3d render

the assembly picture above is the render. a step file is built by github actions for anyone who wants to open the model in their own cad tool.

## specs of the test rig

| item | value |
|---|---|
| motor | 150 W dc, 3000 rpm |
| gearbox | two stage spur gears, 25 to 1 total |
| gear module | 1.5, with 16 tooth and 80 tooth gears |
| output speed | 120 compressions per minute |
| mechanism | scotch yoke, 25 mm crank radius |
| stroke | 50 mm |
| peak force | about 500 N |
| frame | wood |

## materials, prices and links

prices were checked on 25 november 2026 and are in us dollars. they change, so check the link before you order.

| part | qty | price each | link |
|---|---|---|---|
| 16 tooth steel spur gear, module 1.5, 8 mm bore | 2 | $19.99 | [zoro](https://www.zoro.com/khk-usa-steel-spur-gears-ss15-16b/i/G104670229) |
| 80 tooth steel spur gear, module 1.5, 15 mm bore | 2 | $89.29 | [zoro](https://www.zoro.com/khk-usa-hubless-steel-spur-gears-ssa15-80/i/G304670562/) |
| 20 A pwm dc motor speed controller | 1 | $8.72 | [ebay](https://www.ebay.com/itm/12V-24V-Max-20A-PWM-DC-Motor-Stepless-Variable-Speed-Control-Controller-Switch-/111936836128) |
| 24 V 15 A power supply (mean well lrs 350 24) | 1 | $31.35 | [bravo electro](https://www.bravoelectro.com/lrs-350-24.html) |
| 8 mm precision ground rotary shaft | 1 m | $6.50 | [phidgets](https://phidgets.com/?prodid=875) |
| pillow block bearings for 8 mm shaft, pack of 2 | 2 packs | $4.25 | [phidgets](https://phidgets.com/?prodid=875) |
| 150 W 24 V dc motor, about 3000 rpm | 1 | not priced yet | see note below |
| plywood for the frame, pad and yoke | 1 | not priced yet | local hardware store |

the priced parts add up to about $273.63 before shipping and tax. the motor and wood are not included in that number, so the real total is higher.

### things to know about this list

the motor is the open item. i could not find a 150 W, 24 V, 3000 rpm brushed motor with a clear price. options i found were a discontinued rs pro 156 W motor at 3000 rpm, a maxon 150 W motor that spins at 7580 rpm (wrong speed, it would change the gear ratio), and a neoton 150 W brushless motor at 3000 rpm with no price shown. the team needs to pick one and update this table.

the gear quantities assume the two stage 25 to 1 gearbox uses two 16 tooth and two 80 tooth gears. the 80 tooth gear has a 15 mm bore and the shafts here are 8 mm, so the bores and shaft sizes in cprisef.py must be matched before ordering.

the speed controller listed is a generic one, not a medical or lab grade part.

## safety and ethics

no human participants are involved. the rig is only ever tested on a manikin or a force sensor, never on a person. no results exist yet, this repo is the design and plan. cprisef is a science fair project and is not a medical device. it must not be used on a real patient. the project will follow the isef rules on safety, ethics, academic integrity and the use of generative ai, and any design or source that inspired it will be credited in the project paperwork.
