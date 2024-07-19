import xml.etree.ElementTree as ET

def filter_vehicles(input_file, output_file, cutoff_time):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Find all vehicle elements
    vehicles = root.findall(".//vehicle")

    # Remove vehicles with depart time >= cutoff_time
    for vehicle in vehicles:
        depart_time = float(vehicle.get('depart'))
        if depart_time >= cutoff_time:
            root.remove(vehicle)

    # Write the modified XML to a new file
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)

# Use the function
input_file = "M50_emitters.emi.xml"
output_file = "M50_emitters_filtered.emi.xml"
cutoff_time = 65700

filter_vehicles(input_file, output_file, cutoff_time)
print(f"Filtered XML saved to {output_file}")