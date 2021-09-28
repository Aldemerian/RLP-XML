import sqlite3
import uuid
'''
sqliteConnection = sqlite3.connect('SQLite_Python.db')
cursor = sqliteConnection.cursor()
sql_command = """
    CREATE TABLE SqliteDb_developers ( 
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128),
    email VARCHAR(128),
    joining_date VARCHAR(128),
    salary VARCHAR(128));"""
cursor.execute(sql_command)
sqliteConnection.commit()
print("create table")
cursor.close()
'''
tupleSkills=[
(1,'Interkulturelle kommunikative Kompetenz', 'Neu Griechisch', 'Berlin-Brandenburg', 'EL-K2-1-EFGH'),
(2,'Text- und Medienkompetenz', 'Neu Griechisch', 'Berlin-Brandenburg', 'EL-K3-1-H'),
(3,'Sprachbewusstheit', 'Neu Griechisch', 'Berlin-Brandenburg', 'EL-K4-1-H'),
(4,'Sprachlernkompetenz', 'Neu Griechisch', 'Berlin-Brandenburg', 'EL-K5-1-EFGH')
]

def insertVaribleIntoTable(skill):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO SqliteDb_developers
                          (id, name, email, joining_date, salary) 
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = skill
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

for skill in tupleSkills:
    print(skill)
    insertVaribleIntoTable(skill)
    
#insertVaribleIntoTable(4, 'Joe', 'joe@pynative.com', '2019-05-19', 9000)
#insertVaribleIntoTable(3, 'Ben', 'ben@pynative.com', '2019-02-23', 9500)