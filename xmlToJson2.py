import xml.etree.ElementTree as ET
import json
import html
import uuid
from functools import reduce

demo=input("Give me your Poor, your huddled XML-File_Path: ")

fileInput = demo[20:29]
fileInput = fileInput.rstrip(".xml")
print(fileInput)
f = open(demo, "r")
#for file name configure rest
#ask which of the 4 this is
#skills
tree = ET.parse(f)

#print("competence")
nodes = tree.findall('./{http://bsbb.eu}c2/')
fachType = tree.getroot()
print(fachType[1].text)
varFach = fachType[1].text
varCategory = input("Which category is this? (Logik, Sprache, Soziales, Bewegung)")
correctNode = nodes
skillUUID = ""
#print(skillUUID)
skillId = 1
skillName = ""
skillAltName = ""
skillComp = ""
sampleNode = ""
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
                print(skill.text)
                for subskill in skill:
                    if subskill.tag == '{http://bsbb.eu}level':
                        skillComp = subskill.text
                    #print(subskill.text)
                    for subsubskill in subskill:
                        #print(subsubskill.text)
                        if subsubskill.tag == '{http://bsbb.eu}id':
                            skillAltName = subsubskill.text
                            #print(skillId)
                        elif subsubskill.tag == '{http://bsbb.eu}content':
                            skillName = html.escape(subsubskill.text)
                            skillUUID = uuid.uuid4()
                            #print(skillUUID)
                            outputComp={
                                "@type":"competence",
                                "id": str(skillUUID),
                                "name":skillName,
                                "fach": varFach,
                                "level":skillComp,
                                "alter":"",
                                "schultyp":"",
                                "bundesland": "Berlin-Brandenburg",
                                "alternateName": [skillName, skillAltName],
                                "category": varCategory,
                                "competence":category,
                                "description":"",
                                "klasse":"",
                                "url":""
                            }
                            #skillId += 1
                            #print(outputComp)
                            allSkills.append(outputComp)

#print(allSkills[2]['name'])
#print("end competence")

#print("skills")
nodes = tree.findall('./{http://bsbb.eu}c3/{http://bsbb.eu}themainhalt/')

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
            if type(skillName) == type(None):
                continue
            #mask all Sonderzeichen!!
            outputSkill={
                    "@type":"skill",
                    "id": str(skillUUID),
                    "name":html.escape(skillName),
                    "fach":varFach,
                    "level":"",
                    "alter":"",
                    "schultyp":"",
                    "bundesland": "Berlin-Brandenburg",
                    "alternateName": [skillName, skillAltName],
                    "category":varCategory,
                    "competence": comp1,
                    "description":"",
                    "klasse":"",
                    "url":""
                }
            #skillId2 = str(skillId)
            allSkills.append(outputSkill)
            skillId += 1

#print(allSkills[50])
varReturn = []
varNode = []
sampleNode = ""
sampleReturn = ""
createCypher = ""
enumSkill = 1
for n in allSkills:
    varNode.append('(u'+str(enumSkill)+':Skill{uuid:"'+n['id']+'", name:"' +n['name'] + '", fach:"'+n['fach']+'", level:"'+n['level']+'", bundesland:"'+n['bundesland']+'", competence:"'+n['competence']+'"})')
    #varReturn2 = 'u'+str(n['id'])+' '
    varReturn.append('u'+str(enumSkill))
    #sampleNode='Create (u'+str(n['id'])+':Skill{name:"' +n['name'] +'"}) SET u.id="'+str(n['id'])+'", u.fach="'+n['fach']+'", u.level="'+n['level']+'", u.bundesland="'+n['bundesland']+'", u.subcategory="'+n['subcategory']+'";\n'
    enumSkill += 1
varNode = str(varNode).strip("[]")
varReturn =  str(varReturn).strip("[]")
varNode = varNode.replace("'","")
varReturn = varReturn.replace("'","")
varNode = varNode.replace("\n","")
varReturn = varReturn.replace("\n","")
sampleNode = "Create "+varNode+"\n"
sampleReturn = 'return '+varReturn
createCypher = sampleNode + sampleReturn
print(createCypher)


'''MATCH
  (a:Person),
  (b:Person)
WHERE a.name = 'A' AND b.name = 'B'
CREATE (a)-[r:RELTYPE]->(b)
RETURN type(r)'''


dataname1 = "/home/maike/RLP-XML/" + fileInput + ".txt"
with open(dataname1, 'w') as d:
    d.writelines(createCypher)
    
dataname2 = "/home/maike/RLP-XML/" + fileInput + ".json"
allSkills = json.dumps(allSkills)
with open(dataname2, 'w') as g:
    g.writelines(allSkills)
