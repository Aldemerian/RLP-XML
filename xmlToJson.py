import xml.etree.ElementTree as ET

demo=input("Give me your Poor, your huddled XML-File_Path: ")

f = open(demo, "r")
print(f.read()) 

tree = ET.parse(f)
root = tree.getroot()
for subarea in root.iter('subarea'):
	print(subarea.attrib)
	for sub in subarea.iter("competence"):
		print(sub.attrib)
		for comp in sub.iter("standard"):
			print(comp.attrib)
			for skill in comp:
				skillId=skillId++
				outputSkill={"id": skillId,
					     "name":skill.name.attrib,
					     "fach":"Mathe",
					     "alter":"",
					     "location": {
						     "bundesland": "Berlin-Brandenburg"
					     },
					     "alternateName": [skill.id.attrib, skill.name.attrib, skill.name.content],
					     "category":"Logik",
					     "subcategory":sub.name.attrib,
					     "bloom": skill.stufe.level.attrib,
					     "competence":comp.name.attrib,
					     "description":"",
					     "klasse":"",
					     "url":""
					    }
				print(outputSkill)
				allSkills.append(outputSkill)
				
				
print(allSkills)
