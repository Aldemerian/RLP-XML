#import json
import os
from xml.etree import ElementTree
import sqlite3
import html

categoryInput = dict([
    ("bio.xml","Logik"),
    ("jp.xml","Kommunikation"),
    ("teilb.xml","Soziales"),
    ("GEWI.xml","Soziales"),
    ("rlp110.xml","Soziales"),
    ("nw56.xml","Logik"),
    ("he.xml","Kommunikation"),
    ("el.xml","Kommunikation"),
    ("de.xml","Kommunikation"),
    ("pl.xml","Kommunikation"),
    ("gewi.xml","Soziales"),
    ("bcm.xml","Soziales"),
    ("PB.xml","Soziales"),
    ("zh.xml","Kommunikation"),
    ("it.xml","Kommunikation"),
    ("fr.xml","Kommunikation"),
    ("tr.xml","Kommunikation"),
    ("ru.xml","Kommunikation"),
    ("sw.xml","Kommunikation"),
    ("fs.xml","Kommunikation"),
    ("La.xml","Kommunikation"),
    ("es.xml","Kommunikation"),
    ("en.xml","Kommunikation"),
    ("agr.xml","Kommunikation"),
    ("bcs.xml","Kommunikation"),
    ("pt.xml","Kommunikation"),
    ("dgs.xml","Kommunikation"),
    ("Deutsch.xml","Kommunikation"),
    ("ch.xml","Logik"),
    ("AS.xml","Logik"),
    ("wat.xml","Logik"),
    ("ku.xml","Logik"),
    ("ma.xml","Logik"),
    ("GEO.xml","Logik"),
    ("geo.xml","Logik"),
    ("nw.xml","Logik"),
    ("Phil.xml","Logik"),
    ("Ph.xml","Logik"),
    ("MU.xml","Logik"),
    ("Inf.xml","Logik"),
    ("L-E-R.xml","Soziales"),
    ("Psy.xml","Soziales"),
    ("eth.xml","Soziales"),
    ("su.xml","Soziales"),
    ("ge.xml","Soziales"),
    ("teila.xml","Soziales"),
    ("sowiwiwi.xml","Soziales"),
    ("thea.xml","Bewegung"),
    ("Thea.xml","Bewegung")])
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
            #print("competence")
            sql_command = """INSERT INTO competence
                VALUES (?,?,?,?,?);"""
        elif varTable == "skill":
            #print("skill")
            sql_command = """INSERT INTO skill
                VALUES (?,?,?,?,?);"""
        elif varTable == "topic":
            #print("topic")
            sql_command = """INSERT INTO topic
                VALUES (?,?,?,?,?,?);""" 
        connection.executemany(sql_command, allwhateva)
        connection.commit()
        #print("Python Variables inserted successfully into SqliteDb_developers table")
        """
        for row in cursor.execute("SELECT * FROM competence"):
            print(row)
        """
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
    if varFach == "Musik" or varFach == "Geschichte" or varFach == "Deutsche Gebärdensprache" \
       or varFach == "Latein" or varFach == "Politische Bildung" or varFach == "Philosophie" \
       or varFach == "Theater" or varFach == "Psychologie" or varFach == "Informatik" \
       or varFach == "Altgriechisch" or varFach=="Lebensgestaltung-Ethik-Religionskunde" \
       or varFach == "Deutsch" or varFach == "Kunst" or varFach == "Gesellschaftswissenschaften":
        print("this is Music")
        good_bot = tryNodes.findall('./c2/area/')
        for item in good_bot:
            #print(item.tag + ": " + item.text)
            compId = ""
            compName = ""
            for ites in item:
                #print(ites.tag + " 2: " + ites.text)
                #print(iter.tag + ": " + iter.text)
                if ites.tag == "name":
                    if ites.text is not None:
                        compName = html.escape(ites.text)
                if ites.tag == "id":
                    if ites.text is not None:
                        compId = html.escape(ites.text)
                if ites.tag == "stufe":
                    for stufe in ites:
                        skillsid=""
                        skillsname=""
                        for standard in stufe:
                            #print("worked")
                            if standard.tag == "id":
                                skillsid=html.escape(standard.text)
                            if standard.tag == "content":
                                skillsname=html.escape(standard.text)
                        if skillsid!="" and skillsname!="":
                            skillId.append(skillsid)
                            skillName.append(skillsname)
            if compId != "" and compName != "":
                competenceName.append(compName)
                competenceId.append(compId)
                #print("worked")
                #print(compId + ": " + compName)
    else:
        good_bot = tryNodes.findall('./c2/area/')
        for item in good_bot:
            for ites in item:
                compId = ""
                compName = ""
                for iter in ites:
                    if iter.tag == "name":
                        if iter.text is not None:
                            compName = html.escape(iter.text)
                    if iter.tag == "id":
                        if iter.text is not None:
                            compId = html.escape(iter.text)
                    if iter.tag == "stufe":
                        for stufe in iter:
                            skillsid=""
                            skillsname=""
                            for standard in stufe:
                                #print("worked")
                                if standard.tag == "id":
                                    skillsid=html.escape(standard.text)
                                if standard.tag == "content":
                                    skillsname=html.escape(standard.text)
                            if skillsid!="" and skillsname!="":
                                skillId.append(skillsid)
                                skillName.append(skillsname)
                if compId != "" and compName != "":
                    competenceName.append(compName)
                    competenceId.append(compId)
                    #print("worked")
                    #print(compId + ": " + compName)
    """        
    allNodes = tryNodes.findall('./c2/area/competence/name')
    #competence name
    for item in allNodes:
        competenceName.append(html.escape(item.text))
    allNodes = tryNodes.findall('./c2/area/competence/id')
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
    """
    if fileExceptionName == "GEO.xml" or fileExceptionName == "geo.xml":
        return
    if len(competenceName) == 0:
        allNodes = tryNodes.findall('./c2/area/name')
        for item in allNodes:
            competenceName.append(html.escape(item.text))
    if len(competenceId) == 0:
        allNodes = tryNodes.findall('./c2/area/id')
        for item in allNodes:
            competenceName.append(html.escape(item.text))
    print(len(competenceId))
    print(competenceId)
    print(len(competenceName))
    print(competenceName)
    """
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
        #print("basst scho")
        for ele in range (0,len(skillId)):
            element = (skillId[ele],skillName[ele], varFach, "Berlin-Brandenburg", varCategory)
            allSkills.append(element)
    if len(competenceId) == len(competenceName):
        #print("basst scho, aber bei competence")
        for ele in range (0,len(competenceId)):
            element = (competenceId[ele],competenceName[ele], varFach, "Berlin-Brandenburg", varCategory)
            allCompetences.append(element)
    if len(topicId) == len(topicName):
        #print("basst scho, aber bei topics, hier weiter")
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
                varCategory=categoryInput[entry.name]
                #print(varCategory)
                varFach = fachType[1].text
                goDeep(tree, varCategory, varFach, entry.name)
                f.close()
                
writetoDB(allCompetences, "competence")
writetoDB(allSkills, "skill")
writetoDB(allTopics, "topic")
                           
#print(allCompetences)
#print(allSkills)
#print(allTopics)
