## Example reading output from sensors and logging it

Copy the files to your device and log.sh to your crontab
```bash
*/1 * * * * /var/scripts/sensors/log.sh
```

**log.py** runs "sensors" on the device and parses the output. If it fails to connect it writes the content to ./data/<timestamp>.json

**process-fails.py** scans the ./data/ directory for json files and attempts the request again. If successful it deletes
the file(s), if not it's left to try again later

**log.sh** runs log.py followed by process-fails.py

Example output used in the log.py example. Modify log.py to suit your needs.

```bash
~# sensors
k10temp-pci-00c3
Adapter: PCI adapter
temp1:        +10.2°C  (high = +70.0°C)
                       (crit = +90.0°C, hyst = +87.0°C)

it8721-isa-0290
Adapter: ISA adapter
in0:          +2.80 V  (min =  +0.72 V, max =  +0.61 V)  ALARM
in1:          +2.76 V  (min =  +2.33 V, max =  +0.11 V)  ALARM
in2:          +1.31 V  (min =  +2.34 V, max =  +0.24 V)  ALARM
+3.3V:        +3.17 V  (min =  +4.13 V, max =  +2.83 V)  ALARM
in4:          +0.00 V  (min =  +0.64 V, max =  +1.78 V)  ALARM
in5:          +2.52 V  (min =  +1.63 V, max =  +0.42 V)  ALARM
in6:          +0.00 V  (min =  +0.43 V, max =  +1.82 V)  ALARM
3VSB:         +1.68 V  (min =  +0.29 V, max =  +3.22 V)
Vbat:         +3.36 V  
fan1:         621 RPM  (min =   19 RPM)
fan2:           0 RPM  (min =   86 RPM)  ALARM
fan3:           0 RPM  (min =  464 RPM)  ALARM
temp1:        +29.0°C  (low  = +32.0°C, high = -105.0°C)  ALARM  sensor = thermistor
temp2:        +16.0°C  (low  =  +9.0°C, high = -111.0°C)  ALARM  sensor = thermistor
temp3:       -128.0°C  (low  = +79.0°C, high = +16.0°C)  sensor = disabled
intrusion0:  OK

qlcnic-pci-0100
Adapter: PCI adapter
temp1:        +35.0°C  

fam15h_power-pci-00c4
Adapter: PCI adapter
power1:       46.53 W  (crit = 124.95 W)

qlcnic-pci-0101
Adapter: PCI adapter
temp1:        +35.0°C
```
