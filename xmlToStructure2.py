#import json
import os
from xml.etree import ElementTree
import sqlite3
import html

allCompetences = []
allSkills = []
allTopics = []

def flushDB ():
    connection = sqlite3.connect("/home/maike/RLP-XML/skills.db")
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE competence;""")
    cursor.execute("""DROP TABLE skill;""")
    cursor.execute("""DROP TABLE topic;""")

def createDB ():
    connection = sqlite3.connect("/home/maike/RLP-XML/skills.db")
    cursor = connection.cursor()
    #insert unique again! primary key!
    sql_command = """
        CREATE TABLE competence ( 
        alternateName VARCHAR(128),
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    sql_command = """
        CREATE TABLE skill (
        alternateName VARCHAR(128),
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    sql_command = """
        CREATE TABLE topic (
        alternateName VARCHAR(128),
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        content TEXT,
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    # never forget this, if you want the changes to be saved:
    connection.commit()
    connection.close()

def writetoDB(allwhateva, varTable):
    try:
        connection = sqlite3.connect("/home/maike/RLP-XML/skills.db")
        cursor = connection.cursor()
        print("Connected to SQLite")
        sql_command = ""
        if varTable == "competence":
            print("competence")
            sql_command = """INSERT INTO competence
                VALUES (?,?,?,?,?);"""
        elif varTable == "skill":
            print("skill")
            sql_command = """INSERT INTO skill
                VALUES (?,?,?,?,?);"""
        elif varTable == "topic":
            print("topic")
            sql_command = """INSERT INTO topic
                VALUES (?,?,?,?,?,?);""" 
        connection.executemany(sql_command, allwhateva)
        connection.commit()
        #print("Python Variables inserted successfully into SqliteDb_developers table")
        for row in cursor.execute("SELECT * FROM competence"):
            print(row)
        connection.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")
            #quit()

def goDeep(tree, varCategory, varFach, fileExceptionName):
    competenceName= []
    competenceId= []
    skillId=[]
    skillName=[]
    topicId=[]
    topicName=[]
    topicContent=[]
    tryNodes = tree.getroot()
    allNodes = tryNodes.findall('./c2/area/competence/stufe/name')
    #competence name
    for item in allNodes:
        competenceName.append(html.escape(item.text))
    allNodes = tryNodes.findall('./c2/area/competence/stufe/id')
    #competence id?
    for item in allNodes:
        competenceId.append(html.escape(item.text))
    allNodes = tryNodes.findall('./c2/area/competence/stufe/standard/id')
    #skill id
    for item in allNodes:
        skillId.append(html.escape(item.text))
    allNodes = tryNodes.findall('./c2/area/competence/stufe/standard/content')
    #skill name
    for item in allNodes:
        skillName.append(html.escape(item.text))
    if fileExceptionName == "GEO.xml" or fileExceptionName == "geo.xml":
        return
    """
    allNodes = tryNodes.findall('./c2/competence/stufe/name')
    #Nwithout area tag
    for item in allNodes:
        competenceId.append(html.escape(item.text))
    allNodes = tryNodes.findall('./c2/area/competence/stufe/standard/content')
    for item in allNodes:
        skillName.append(html.escape(item.text))
    allNodes = tryNodes.findall('./c2/area/name')
    for item in allNodes:
        competenceName.append(html.escape(item.text))
    allNodes = tryNodes.findall('./c2/area/id')
    for item in allNodes:
        competenceName.append(html.escape(item.text))

    /bc/bc3/area[1]/competence[1]/name
    """
    allNodes = tryNodes.findall('./c3/themainhalt/id')
    for node in allNodes:
        topicId.append(html.escape(node.text))
    allNodes = tryNodes.findall('./c3/themainhalt/title')
    for node in allNodes:
        topicName.append(html.escape(node.text))
    allNodes = tryNodes.findall('./c3/themainhalt/content')
    for node in allNodes:
        topicContent.append(html.escape(node.text))
    if len(skillId) == len(skillName):
        print("basst scho")
        for ele in range (0,len(skillId)):
            element = (skillId[ele],skillName[ele], varFach, "Berlin-Brandenburg", varCategory)
            allSkills.append(element)
    if len(competenceId) == len(competenceName):
        print("basst scho, aber bei competence")
        for ele in range (0,len(competenceId)):
            element = (competenceId[ele],competenceName[ele], varFach, "Berlin-Brandenburg", varCategory)
            allCompetences.append(element)
    if len(topicId) == len(topicName):
        print("basst scho, aber bei topics, hier weiter")
        if len(topicId) == len(topicContent):
            for ele in range (0,len(topicId)):
                element = (topicId[ele],topicName[ele], varFach, "Berlin-Brandenburg", topicContent[ele], varCategory)
                allTopics.append(element)

flushDB()
createDB()

basepath = "/home/maike/RLP-XML/"
with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.is_file():
            fileExtension = os.path.splitext(entry.name)
            print(entry.name)
            if fileExtension[1] == '.xml':
                f = open(entry, "r")
                try:
                    tree = ElementTree.parse(f)
                    fachType = tree.getroot()
                    print(fachType[1].text)
                except ElementTree.ParseError as e:
                    print(e)
                varCategory=""
                varCategory = input("Which category is this? (1=Logik, 2=Kommunikation, 3=Soziales, 4=Bewegung)")
                if varCategory == "1":
                    varCategory = "Logik"
                elif varCategory == "2":
                    varCategory = "Kommunikation"
                elif varCategory == "3":
                    varCategory = "Soziales"
                elif varCategory == "4":
                    varCategory = "Bewegung"
                print(varCategory)
                varFach = fachType[1].text
                goDeep(tree, varCategory, varFach, entry.name)
                f.close()
                
#worked when it was still indented. why? whhhyyyy?
writetoDB(allCompetences, "competence")
writetoDB(allSkills, "skill")
writetoDB(allTopics, "topic")
                
             
print(allCompetences)
print(allSkills)
print(allTopics)
