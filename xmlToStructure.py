#import json
import os
from xml.etree import ElementTree
import uuid
import sqlite3
import html

allSkills = []

def flushDB ():
    connection = sqlite3.connect("/home/maike/RLP-XML/skills.db")
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE competence;""")
    cursor.execute("""DROP TABLE skill;""")
    cursor.execute("""DROP TABLE topic;""")

def createDB ():
    connection = sqlite3.connect("/home/maike/RLP-XML/skills.db")
    cursor = connection.cursor()
    # uuid hinzu und id="k-1" speichern als verarbeitungsvariable
    sql_command = """
        CREATE TABLE competence ( 
        alternateName VARCHAR(128) PRIMARY KEY Unique,
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        subCategory Text,
        num_skills INT,
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    sql_command = """
        CREATE TABLE skill ( 
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        alternateName VARCHAR(128) PRIMARY KEY,
        uuid_competence VARCHAR(36),
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    sql_command = """
        CREATE TABLE topic ( 
        name VARCHAR(128),
        fach VARCHAR(128),
        bundesland VARCHAR(128),
        alternateName VARCHAR(128) PRIMARY KEY,
        content TEXT,
        category VARCHAR(20));"""
    cursor.execute(sql_command)
    # never forget this, if you want the changes to be saved:
    connection.commit()
    connection.close()

def writetoDB(allSkills):
    try:
        connection = sqlite3.connect("/home/maike/RLP-XML/skills.db")
        cursor = connection.cursor()
        print("Connected to SQLite")
        sql_command = """INSERT INTO competence
                VALUES (?,?,?,?,?,?,?);"""
        connection.executemany(sql_command, allSkills)
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

def goDeep(tree, varCategory, varFach):
    tryNodes = tree.getroot()
    allNodes = tryNodes.findall('./c2/area')
    for area in allNodes:
        #print(area.tag)
        if area.tag == "area":
            for competence in area:
                #print(competence.tag)
                #if competence.tag == "id":
                    #print("competence id: " + competence.text)
                if competence.tag == "name":
                    #print("competence name: " + competence.text)
                    subcategory = html.escape(competence.text)
                #if competence.tag == "area":
                    #print("wut?")
                if competence.tag == "competence":
                    for stufe in competence:
                        #varCompetenceID = uuid.uuid4()
                        lengthSkills= 0
                        if stufe.tag == "id":
                            #print(stufe.text)
                            varCompetenceExID = html.escape(stufe.text)
                        if stufe.tag == "name":
                            varCompetence = html.escape(stufe.text)
                            if varFach == "Polnisch":
                                print(stufe.text)
                        if stufe.tag == "stufe":
                            for standard in stufe:
                                if standard.tag == "id":
                                    #print(standard.text)
                                    varCompetenceExID = html.escape(standard.text)
                                #if standard.tag == "level":
                                    #print(standard.text)
                                if standard.tag == "standard":
                                    lengthSkills =  len(standard)
                                    for content in standard:
                                        #if content.tag == "id":
                                            #print("skillid:" + content.text)
                                        if content.tag == "content":
                                            #print("skillname: " + content.text)
                                            html.escape(content.text)
                    #varCompetence = html.escape(stufe.text)
                    collectSkill = (varCompetenceExID, varCompetence, varFach,"Berlin-Brandenburg", subcategory, lengthSkills,varCategory)
                    allSkills.append(collectSkill)
        if area.tag == "competence":
            '''hier weiter siehe NT56'''
            for competence in area:
                print(competence.text)
                #if competence.tag == "id":
                    #print("competence id: " + competence.text)
                if competence.tag == "name":
                    #print("competence name: " + competence.text)
                    subcategory = html.escape(competence.text)
                if competence.tag == "stufe":
                    for stufe in competence:
                        print(stufe.text)
                        varCompetenceID = uuid.uuid4()
                        lengthSkills= 0
                        lengthSkills =  len(stufe)
                        if stufe.tag == "id":
                            varCompetenceExID = html.escape(stufe.text)
                        if stufe.tag == "name":
                            varCompetence = html.escape(stufe.text)
                        if stufe.tag == "standard":
                            for content in standard:
                                print("skillid:" + content.text)
                                #if content.tag == "id":
                                    #print("skillid:" + content.text)
                                if content.tag == "content":
                                    #print("skillname: " + content.text)
                                    html.escape(content.text)
                    #varCompetence = html.escape(stufe.text)
                    collectSkill = (varCompetenceExID, varCompetence, varFach,"Berlin-Brandenburg", subcategory, lengthSkills,varCategory)
                    allSkills.append(collectSkill)

    '''        
    allNodes = tryNodes.findall('./c3/themainhalt')
    for node in allNodes:
        print(node.tag)
        for item in node:
            if item.tag == "id":
                print("topicid: "+item.text)
            if item.tag == "title":
                print("topicname: "+item.text)
            if item.tag == "content":
                print("topiccontent: "+item.text)
'''

flushDB()
createDB()
                
basepath = "/home/maike/RLP-XML/"
with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.is_file():
            fileExtension = os.path.splitext(entry.name)
            if fileExtension[1] == '.xml':
                f = open(entry, "r")
                tree = ElementTree.parse(f)
                fachType = tree.getroot()
                print(fachType[1].text)
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
                goDeep(tree, varCategory, varFach)
                f.close()
                writetoDB(allSkills)