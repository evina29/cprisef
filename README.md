# automatic cpr rig with ai guidance

cardiac arrest kills most of the people it hits, and a lot of that comes down to cpr not being good enough or not starting fast enough. this project is our answer: a machine that does chest compressions for you, with ai guidance and help to make the whole thing easier to use under pressure.

this repo holds the cad for our test rig, which is the part that does the pushing, plus the code that builds it.

## the problem

every year there are over 350,000 cardiac arrests outside hospitals in the us and over 270,000 in the eu, and around 90 percent of them are fatal. a big reason is not enough cpr, either because bystanders are not doing it well or because help arrives late. doing compressions by hand is exhausting, and tired hands make mistakes.

the machines that exist today are not great either. the main one is bulky, costs around 20,000 dollars, does not fit large patients, and can cause more skin damage and rib fractures than doing it by hand. we think a cheaper, smaller and softer machine is possible.

## what we are building

an automatic, hands free cpr device that is light enough to carry, cheap to make, and soft on the patient, with ai guidance and help on top. we will write up the ai part here as we build it.

## what is in this repo

cpr_rig.py builds our test rig as a 14 part assembly in millimetres and saves it as a step file. you can open that in onshape, fusion, solidworks or freecad.

```
pip install -r requirements.txt
python cpr_rig.py cpr_lifeline_rig.step
```

you get one step file and one stl file for each main part. to use it in onshape, press create, then import, then pick the step file.

if you do not want to set anything up, open the actions tab on github, run the build step workflow, and download the files it makes.

all the sizes are plain variables at the top of cpr_rig.py. change them and run it again to get a new model.

## screenshots

### full 3d assembly

![3d assembly of the test rig seen from the gear side](docs/assembly.svg)

wood frame, 150 watt motor, two stage gear train that slows it down 25 to 1, the yoke, the rod and the microfiber pad. the gears are drawn as simple discs in this picture. the step file has real toothed gears.

### wiring diagram

![wiring diagram showing a bench power supply connected to the motor](docs/wiring.svg)

### pcb

there is no pcb yet. the motor runs straight from a bench power supply.

### 3d render

the assembly picture above is the render.

## specs of the test rig

* motor: 150 watt dc, 3000 rpm
* gearbox: two stages of 16 teeth into 80 teeth, which makes 25 to 1
* output: 120 rpm, so 120 compressions a minute
* crank radius: 25 mm, which gives about 2 inches of travel
* force target: about 500 newtons
* pad: 80 mm wide and 15 mm thick, made of microfiber
* frame: a wooden table, with the other parts 3d printed

the frame size, wood sizes, motor body size, gear widths and tooth shape are estimates and can be changed.

## not a medical device

this is a cad and software project. it has not been tested or approved as medical equipment and it must never be used on a person.
# cpr lifeline rig, plus ai guidance

this project builds on the cpr lifeline idea: a machine that does chest compressions for you, held on with a padded strap that fits any chest size. we are not trying to validate the original cpr lifeline. we took its idea and its prototype as a starting point, and we are adding ai guidance and help on top of it.

all credit for the cpr lifeline concept, its specs and the background numbers below goes to the original cpr lifeline project. the cad in this repo is our own model of their test rig, rebuilt from the numbers they gave in their video.

## what it is and how to use it

cpr_rig.py builds the whole rig as a 14 part assembly in millimetres and saves it as a step file. you can open that in onshape, fusion, solidworks or freecad.

```
pip install -r requirements.txt
python cpr_rig.py cpr_lifeline_rig.step
```

you get cpr_lifeline_rig.step and one stl file for each main part. to use it in onshape, press create, then import, then pick the step file.

if you do not want to set anything up, open the actions tab on github, run the build step workflow, and download the files it makes.

all the sizes are plain variables at the top of cpr_rig.py. change them and run it again to get a new model.

## why we made it

these numbers come from the cpr lifeline project. every year there are over 350,000 cardiac arrests outside hospitals in the us and over 270,000 in the eu, and around 90 percent of them are fatal. a big reason is not enough cpr, either because bystanders are not doing it well or because help arrives late. a machine that does it automatically would save time and effort and let medical teams focus on other care.

they compared their idea to the lucas device, which does not fit large patients, causes more skin damage and rib fractures than manual cpr, and costs about 20,000 dollars. their idea answers that with an adjustable padded strap, soft microfiber pads, a small design that costs about 200 dollars in parts, and room for defibrillation pads so an aed can be used during cpr.

we want to take that idea further by adding ai guidance and help. we will write that part up here as we build it.

## screenshots

### full 3d assembly

![3d assembly of the test rig seen from the gear side](docs/assembly.svg)

wood frame, 150 watt motor, two stage gear train that slows it down 25 to 1, the yoke, the rod and the microfiber pad. the gears are drawn as simple discs in this picture. the step file has real toothed gears.

### wiring diagram

![wiring diagram showing a bench power supply connected to the motor](docs/wiring.svg)

### pcb

there is no pcb yet. the motor runs straight from a bench power supply.

### 3d render

the assembly picture above is the render.

## specs we modelled from the cpr lifeline prototype

* motor: 150 watt dc, 3000 rpm
* gearbox: two stages of 16 teeth into 80 teeth, which makes 25 to 1
* output: 120 rpm, so 120 compressions a minute
* crank radius: 25 mm, which gives about 2 inches of travel
* force target: about 500 newtons
* pad: 80 mm wide and 15 mm thick, made of microfiber
* frame: a wooden table, with the other parts 3d printed

the frame size, wood sizes, motor body size, gear widths and tooth shape are our own estimates and did not come from the video.

## not a medical device

this is a cad and software project. it has not been tested or approved as medical equipment and it must never be used on a person.
