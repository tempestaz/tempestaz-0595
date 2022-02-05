# Voron Filament Sensor Mount

Using one of the standard pre-made microswitch-based filament sensors, this mount attaches typically before the bowden support.

![Filament Sensor Mount image](Photos/Filament_Sensor_Mount.png)

# Bill of Materials (BOM)

Tools:

- Soldering Iron for the heat inserts

Filament mount:

- 1x M3x8 mm
- 1x M3 t-nut or equivalent

Fixed sensor mount:

- 2x M3 heat set insert
- 2x M3x16 mm

# Assembly

## Step 1 - Filament Sensor Mount

For the filament sensor mount you need the following parts:

- 2x M3 heat set insert

Install your heat set threaded inserts using the soldering iron or your preferred tool. Place the inserts on the bottom of the mount so if there is protrusion they will come out the top

<img src="./Photos/Filament_Sensor_Mount_Inserts.png" height="150" /><img src="./Photos/Filament_Sensor_Mount_Inserts_top.png" height="150" style="margin-left:40px" />

## Step 2: Filament Sensor Assembly

For the filament sensor assembly you need the following parts:

- 2x M3x16 mm

Insert the screws through the filament sensor ensuring the orientation of the sensor is as shown in the picture above.

<img src="./Photos/Filament_Sensor_Mount_Assembled.png" height="150" />

## Step 3: Filament Sensor Assembly Mounting

For the completed filament sensor assembly you need the following parts:

- 1x M3x8 mm
- 1x M3 t-nut or equivalent

Insert the M3x8 mm screw through the top and attach the t-nut to the bottom. Install on the frame a couple of inches (50mm) or more from the bowden tube support.

## Step 4: Configure Klipper

Add the following to the printer configuration file.
```
[filament_switch_sensor filament_sensor]
pause_on_runout: True
runout_gcode:
    PARK_MACRO
    M117 Out of Filament
insert_gcode:
    M117 Resuming
    RESUME_MACRO
event_delay: 3.0
pause_delay: 0.5
switch_pin: PG11 #you will need to change this to the actual i/o pin used by the sensor
```

*Note: the **PARK_MACRO** and **RESUME_MACRO** are not defined here. See the Voron users github for macros that may work for you.*
