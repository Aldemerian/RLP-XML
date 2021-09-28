import xml.etree.ElementTree as ET
import json
import html
import uuid
from functools import reduce
import os
import sqlite3

allSkills = []
allCompetences = []

def skillRLPschema (tree):
    #skills with tags
    correctNode = tree.findall('./{http://bsbb.eu}c2/')
    skillUUID = ""
    skillAltName = ""
    comp1 = ""
    skillName = []
    for item in correctNode:
        if item.tag == '{http://bsbb.eu}vorwort':
            continue
        for subitem in item:
            #area
            for subsubitem in subitem:
                #id, name, subarea oder id, name, competence
                if subsubitem.tag == '{http://bsbb.eu}name':
                    comp1 = subsubitem.text
                    print("Competence: "+comp1)
                #if subsubitem.tag == '{http://bsbb.eu}stufe':
                #    if subsubitem.tag == "":
                #        continue
                #    else:
                #        comp1 = subsubitem.text
                #        print("Competence: "+comp1)
                if subitem.tag == '{http://bsbb.eu}competence':
                    skillName = []
                    for subskill in subsubitem:
                        if subskill.tag == '{http://bsbb.eu}name':
                            print("other competence? "+subskill.text)
                        #id, name, stufe
                #if subsubitem.tag == '{http://bsbb.eu}stufe':
                        #id, name, stufe
                        #if subskill.tag == '{http://bsbb.eu}id':
                        #    varLevel = subskill.text
                        #    print(varLevel)
                        if subskill.tag == '{http://bsbb.eu}standard':
                            for subsubskill in subskill:
                                if subsubskill.tag == '{http://bsbb.eu}id':
                                    skillAltName = subsubskill.text
                                    print(skillAltName)
                                if subsubskill.tag == '{http://bsbb.eu}content':
                                    skillName.append(html.escape(subsubskill.text))
                                    print(skillName)
                    skillUUID = uuid.uuid4()
                    outputSkill={
                        "@type":"competence",
                        "id": str(uuid.uuid4()),
                        "name":html.escape(comp1),
                        "fach":varFach,
                        "bundesland": "Berlin-Brandenburg",
                        "alternateName": skillAltName,
                        "category":varCategory,
                        "skills":skillName
                    }
                    allSkills.append(outputSkill)
    
    correctNode = tree.findall('./{http://bsbb.eu}c3/{http://bsbb.eu}themainhalt/')
    for item in correctNode:
        print(item.tag)
        if item.tag=='{http://bsbb.eu}id':
            skillAltName = item.text
        elif item.tag=='{http://bsbb.eu}title':
            skillName = item.text
        elif item.tag=='{http://bsbb.eu}content':
            descrSkill = item.text
        else:
            continue
    outputSkill={
            "@type":"skill",
            "id": str(skillUUID),
            "name": html.escape(comp1),
            "fach": varFach,
            "bundesland": "Berlin-Brandenburg",
            "alternateName": skillAltName,
            "category": varCategory,
            "competence": skillName
        }
    allSkills.append(outputSkill)

def saveToDB ():
    connection = sqlite3.connect("/home/maike/RLP-XML/skills.db")
    cursor = connection.cursor()
    # uuid hinzu und id="k-1" speichern als verarbeitungsvariable
    sql_command = """
        CREATE TABLE competence ( 
        uuid VARCHAR(36) PRIMARY KEY,
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        alternateName VARCHAR(128),
        num_skills INT,
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    sql_command = """
        CREATE TABLE skill ( 
        uuid VARCHAR(36) PRIMARY KEY,
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        alternateName VARCHAR(128),
        uuid_competence VARCHAR(36),
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    sql_command = """
        CREATE TABLE topic ( 
        uuid VARCHAR(36) PRIMARY KEY,
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        content TEXT,
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    for ele in allCompetences:
        '''
        sql_command = """INSERT INTO subcategory (skillcat_uuid, category, finished_last, next_skill, last_skill)
            VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
        cursor.execute(sql_command)
        '''
        cursor.execute(sql_command)
    for ele in allSkills:
        print(ele)
        sql_command = """"""
        cursor.execute(sql_command)
    # never forget this, if you want the changes to be saved:
    connection.commit()
    connection.close()

def chooseRLPSchema (f):
    tree = ET.parse(f)
    decisionTree = tree.getroot()
    print(decisionTree.tag)
    if decisionTree.tag == '{http://bsbb.eu}fach':
        print("with tags")
        skillRLPschema(tree)
    else:
        print("without tags")
        if decisionTree[2].tag == '{http://bsbb.eu}kapitel':
            skillRLPschema2(tree)
        elif decisionTree[2].tag == '{http://bsbb.eu}einleitung':
            skillRLPschema1(tree)
            print(decisionTree[2].tag)
        else:
            print("something went wrong")
    print(allSkills)
    

basepath =input("Give me your Poor, your huddled XML-File_Path: ")

# flush database
connection = sqlite3.connect("/home/maike/RLP-XML/skills.db")
cursor = connection.cursor()
cursor.execute("""DROP TABLE competence;""")
cursor.execute("""DROP TABLE skill;""")
cursor.execute("""DROP TABLE topic;""")


# List all files in a the using scandir()
with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.is_file():
            fileExtension = os.path.splitext(entry.name)
            if fileExtension[1] == '.xml':
                f = open(entry, "r")
                fachType = tree.getroot()
                print(fachType[1].text)
                varFach = fachType[1].text
                varCategory = input("Which category is this? (Logik, Sprache, Soziales, Bewegung)")
                skillRLPschema(tree)
                saveToDB()

