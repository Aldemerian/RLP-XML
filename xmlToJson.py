import xml.etree.ElementTree as ET
import json

#demo=input("Give me your Poor, your huddled XML-File_Path: ")
f = open("/home/maike/RLP-XML/ma.xml", "r")
#f = open(demo, "r")
#print(f.read()) 
#allSkills=[]

#tree = ET.parse(f)
#root = tree.getroot()
#skills
tree = ET.parse(f)

print("competence")
nodes = tree.findall('./{http://bsbb.eu}c2/')
correctNode = nodes
skillId = ""
skillName = ""
skillComp = ""
f = 2
allSkills=[]
#print(correctNode.findall('./'))
for item in correctNode:
    if item.tag == '{http://bsbb.eu}vorwort':
        continue
    for subitem in item:
        #print(subitem.text)
        for subsubitem in subitem:
            if subsubitem.tag == '{http://bsbb.eu}name':
                category = subsubitem.text
            #print(subsubitem.tag)
            for skill in subsubitem:
                #print(skill.tag)
                for subskill in skill:
                    if subskill.tag == '{http://bsbb.eu}level':
                        skillComp = subskill.text
                    for subsubskill in subskill:
                        #print(subsubskill.tag)
                        if subsubskill.tag == '{http://bsbb.eu}id':
                            skillId = subsubskill.text
                            #print(skillId)
                        elif subsubskill.tag == '{http://bsbb.eu}content':
                            skillName = subsubskill.text
                            outputComp={
                                "@type":"skill",
                                "id": skillId,
                                "name":skillName,
                                "fach":"Mathe",
                                "level":skillComp,
                                "alter":"",
                                "schultyp":"",
                                "bundesland": "Berlin-Brandenburg",
                                "alternateName": [skillName, skillId],
                                "category":"Logik",
                                "subcategory":category,
                                "description":"",
                                "klasse":"",
                                "url":""
                            }
                            #print(outputComp)
                            allSkills.append(outputComp)

print(allSkills[2])
print("end competence")

print("skills")
nodes = tree.findall('./{http://bsbb.eu}c3/{http://bsbb.eu}themainhalt/')
skillId = 1
skillName = ""
skillAltName = ""
comp1 = ""

for node in nodes:
    #print(node.tag)
    for item in node:
        if item.tag == '{http://bsbb.eu}name':
            comp1 = item.text
            print(item.tag)
        #print(item.tag)
        for subitem in item:
            #print(subitem.tag)
            #print(comp1)
            for skill in subitem:
                #print(skill.tag)
                #print(skill.text)
                if skill.tag=='{http://bsbb.eu}id':
                    skillAltName = skill.text
                elif skill.tag=='{http://bsbb.eu}content':
                    skillName = skill.text
                else:
                    continue
            outputSkill={
                    "@type":"skill",
                    "id": skillId,
                    "name":skillName,
                    "fach":"Mathe",
                    "level":"",
                    "alter":"",
                    "schultyp":"",
                    "bundesland": "Berlin-Brandenburg",
                    "alternateName": [skillName, skillAltName],
                    "category":"Logik",
                    "competence": comp1,
                    "description":"",
                    "klasse":"",
                    "url":""
                }
            skillId += 1
            allSkills.append(outputSkill)
    
print(allSkills[50])

allSkills = json.dumps(allSkills)
with open('/home/maike/RLP-XML/ma.json', 'w') as g:
    g.writelines(allSkills)
