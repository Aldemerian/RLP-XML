import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()
for neighbor in root.iter('neighbor'):
	print(neighbor.attrib)
