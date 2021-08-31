import xml.etree.ElementTree as ET

demo=input("Give me your Poor, your huddled XML-File_Path: ")

f = open(demo, "r")
#print(f.read()) 
allSkills=[]

tree = ET.parse(f)
root = tree.getroot()
#print(tree.tag)
for subarea in tree.findall('subarea'):
	print(subarea)
	print("ha")
	for sub in subarea.findall("competence"):
		print(sub)
		print("ho")
		for comp in sub.findall("standard"):
			#print(comp.attrib)
			skillId=1
			print("hi")
			for skill in comp:
				skillId+=skillId
				print(skill)
				outputSkill={"id": skillId,
					     "name":skill.findall("name").attrib,
					     "fach":"Mathe",
					     "alter":"",
					     "location": {
						     "bundesland": "Berlin-Brandenburg"
					     },
					     "alternateName": [skill.findall("id").attrib, skill.name.attrib, skill.name.content],
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


