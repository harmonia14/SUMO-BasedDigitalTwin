# Configuration Files for Transportation Digital Twin

This folder contains configuration files for the Transportation Digital Twin simulation project.

## Files 

1. `emitter_filter.py`: Python script to filter vehicle emitters based on departure time.
2. `M50_simulation_digital_twin.sumo.cfg`: SUMO configuration file for the digital twin simulation.
3. `M50_simulation_physical_entity.sumo.cfg`: SUMO configuration file for the physical entity simulation.

## File Descriptions

### emitter_filter.py

This Python script filters vehicles from an XML file based on a cutoff time. It:
- Parses an input XML file
- Removes vehicles with departure times greater than or equal to a specified cutoff time
- Writes the filtered data to a new XML file

Usage:
```python
python emitter_filter.py

The script is currently set to:

- Input file: "M50_emitters.emi.xml"
- Output file: "M50_emitters_filtered.emi.xml"
- Cutoff time: 65700 seconds

### M50_simulation_digital_twin.sumo.cfg
SUMO configuration file for the digital twin simulation. Key settings include:

- Input files: network, vehicle types, routes, and detectors
- Output files: trip info, statistics, and FCD (Floating Car Data)
- Simulation time: 65697.00 to 65700.00 seconds
- Step length: 0.01 seconds
- TraCI remote port: 51709

### M50_simulation_physical_entity.sumo.cfg
SUMO configuration file for the physical entity simulation. Key settings include:

- Input files: network, vehicle types, routes, filtered emitters, and detectors
- Output files: trip info, statistics, and FCD
- Simulation time: 65697.00 to 65700.00 seconds
- Step length: 0.01 seconds
- TraCI remote port: 57790

### Notes

- Both SUMO configuration files use the same simulation time range and step length.
- The physical entity simulation uses the filtered emitters file (M50_emitters_filtered.emi.xml) created by the emitter_filter.py script.
- SSM (Surrogate Safety Measures) device is configured in both simulations for safety analysis.
- The configuration files are set up for a specific time window (65697.00 to 65700.00 seconds), which corresponds to a 3-second period.

To modify simulation parameters or input/output file paths, edit the respective configuration files.