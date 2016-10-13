import sqlite3
import json

conn = sqlite3.connect('nflpool.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS Teams;

CREATE TABLE Teams (
    name    TEXT NOT NULL UNIQUE,
    id  INTEGER NOT NULL PRIMARY KEY UNIQUE,
    city    TEXT NOT NULL,
    abbreviation  TEXT,
    conference  TEXT,
    division  TEXT
)

''')
conn.commit()
conn.close()

x = 0
y = 0

#Change the name of the file to open to match the query below:
with open('json/20160921-conference-team-standings.json') as file:
    alltext = file.readlines()  #Put each line into a list

for lines in alltext:
    if lines.startswith('{'):
        rawdata = lines
        data = json.loads(rawdata)



#       This code shows it's a list with 16 items - each team!
        teamlist = data["conferenceteamstandings"]["conference"][0]["teamentry"]
#        print(len(teamlist))
#        print(type(teamlist))

        #Create a loop to extract each team name (AFC first, then NFC)

        for afc_team_list in teamlist:
            afc_team_name = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["Name"]
            afc_team_city = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["City"]
            afc_team_id = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["ID"]
            afc_team_abbr = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["Abbreviation"]
#            print((afc_team_name), (afc_team_city), (afc_team_id), (afc_team_abbr))
            x = x + 1


            conn = sqlite3.connect('nflpool.sqlite')
            cur = conn.cursor()

            cur.execute('''INSERT INTO Teams(name, id, city, abbreviation, conference)
                        VALUES(?,?,?,?, "AFC")''', (afc_team_name, afc_team_id, afc_team_city, afc_team_abbr))

            conn.commit()
            conn.close()


        for nfc_team_list in teamlist:
            nfc_team_name = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["Name"]
            nfc_team_city = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["City"]
            nfc_team_id = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["ID"]
            nfc_team_abbr = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["Abbreviation"]
#            print((nfc_team_name), (nfc_team_city), (nfc_team_id), (nfc_team_abbr))
            y = y + 1

            conn = sqlite3.connect('nflpool.sqlite')
            cur = conn.cursor()

            cur.execute('''INSERT OR IGNORE INTO Teams(name, id, city, abbreviation, conference)
                        VALUES(?,?,?,?, "NFC")''', (nfc_team_name, nfc_team_id, nfc_team_city, nfc_team_abbr))

            #INSERT DIVISION NAMES INTO DATABASE
            cur.execute('''UPDATE Teams SET division = "EAST" WHERE id in (48,49,50,51,52,53,54,55)''')
            cur.execute('''UPDATE Teams SET division = "NORTH" WHERE id in (56,57,58,59,60,61,62,63)''')
            cur.execute('''UPDATE Teams SET division = "SOUTH" WHERE id in (64,65,66,67,68,69,70,71)''')
            cur.execute('''UPDATE Teams SET division = "WEST" WHERE id in (72,73,74,75,76,77,78,79,80)''')

            conn.commit()
            conn.close()

#TODO
#Import Dvision Name from another JSON file and insert division name for corresponding team into table

#conn = sqlite3.connect('nflpool.sqlite')
#cur = conn.cursor()



#    conn.commit()
#    conn.close()