import sqlite3
from datetime import datetime as dt
import csv
import time

class DB:

    

    def __init__(self, db_name=""):
        self.db_name = 'thawdb.sqlite'
        self.db = None
        self.db_open = False
        self.srow = 2


    def open(self):
        self.db = sqlite3.connect(self.db_name)
        self.db_open = True

    def close(self):
        if self.db_open:
            self.db.close()
            self.db_open = False

    def create_initial_tables(self):
        if not self.db_open:
            DB.open(self)

        c = self.db.cursor()
        c.execute('''CREATE TABLE probes(id INTEGER PRIMARY KEY NOT NULL, identifier VARCHAR NOT NULL, dateCreated DATETIME, dateModified DATETIME)''')
        c.execute('''CREATE TABLE events(id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, dateCreated DATETIME, dateModified DATETIME)''')
        c.execute('''CREATE TABLE data(id INTEGER PRIMARY KEY, datum DOUBLE NOT NULL, probe_ID INTEGER NOT NULL, event_ID INTEGER NOT NULL, dateCreated DATETIME, dateModified DATETIME)''')
        self.db.commit()
        #DB.close()

    def add_initial_probes(self):
        if not self.db_open:
            DB.open(self)

        c = self.db.cursor()
        now = dt.now()
        sql_string = 'INSERT INTO probes(identifier, dateCreated, dateModified) VALUES (?,?,?)'
        probes=[('ff8dSa1503c0', now, now),('be1d070000&',now,now), ('d40b1d070000a9', now, now) ]
        c.executemany(sql_string, probes)
        self.db.commit()
        #DB.close()

    def list_all_probes(self):
        if not self.db_open:
            DB.open(self)

        c = self.db.cursor()
        sql_string = "SELECT id, identifier, name FROM probes"
        c.execute(sql_string)
        rows = c.fetchall()
        for row in rows:
            print(row)

        #DB.close()

    def add_event(self):
        if not self.db_open:
            DB.open(self)

        e = input("What is event description: ")
        c = self.db.cursor()
        now = dt.now()
        d = (e, now, now)
        sqlString = 'INSERT INTO events(name, dateCreated,dateModified) VALUES (?,?,?)'
        c.execute(sqlString, d)
        self.db.commit()
        #DB.close()

    def list_all_events(self):
        if not self.db_open:
            DB.open(self)
        c = self.db.cursor()
        sqlString = 'SELECT id, name FROM events'
        c.execute(sqlString)
        rows = c.fetchall()
        for row in rows:
            print(row)
        #DB.close()

    def add_data(self, dp, probe, eventID):
        if not self.db_open:
            DB.open(self)
        
        print('datapoint',dp,'probe id',probe,'event',eventID)
        c = self.db.cursor()
        now=dt.now()
        c.execute('''SELECT * from probes''')
        rows = c.fetchall()
        pID = [item for item in rows if probe in item][0][0]
        print('probe id', pID)
        d = (dp, pID, eventID, now, now)
        print(d)
        sql_string = 'INSERT INTO data(datum, probe_ID, event_ID, dateCreated, dateModified) VALUES (?,?,?,?,?)'
        c.execute(sql_string, d)
        print('executed')
        self.db.commit()
        print('committed')
        #DB.close()


    def list_all_data(self, n = None):
        if not self.db_open:
            DB.open(self)

        DB.list_all_events(self)
        a = int(input("Get Data for which event id? "))
        print(a)
        DB.list_all_probes(self)
        b = int(input("List all Data for which probe ID? "))
        c = self.db.cursor()
        sql_string = "SELECT data.id, probes.name, data.datum, date(data.dateCreated), time(data.dateCreated) " \
            + "FROM data INNER JOIN probes ON data.probe_ID = probes.id WHERE data.event_ID = ? AND " \
            + "data.probe_ID = ? ORDER BY data.dateCreated DESC"
        c.execute(sql_string, (a, b))
        rows = c.fetchall()
        if n != None:
            rows = rows[0:n]
        for row in rows:
            print(row)

    def export_all_data(self):
        if not self.db_open:
            DB.open(self)

        DB.list_all_events(self)
        a = int(input("List all Data for which event? "))
        # DB.list_all_probes(self)
        c = self.db.cursor()
        sql_string = "SELECT data.dateCreated, data.datum, probes.identifier FROM data " \
            + " INNER JOIN probes ON data.probe_ID = probes.id WHERE data.event_ID = ?"
        c.execute(sql_string, (a,))
        rows = c.fetchall()
        print('# of rows', len(rows))

        # setup csv
        with open('tempdata.csv', 'w', newline='') as csvfile:
            fieldnames = ['date','probe name','temperature']
            writer = csv.DictWriter(csvfile, dialect="excel", fieldnames=fieldnames)

            # Write data
            writer.writeheader()
            for row in rows:
                writer.writerow({'date':row[0],'probe name':row[2],'temperature':row[1]})

    def export_data(self):
        if not self.db_open:
            DB.open(self)

        DB.list_all_events(self)
        a = int(input("List all Data for which event? "))
        # DB.list_all_probes(self)
        c = self.db.cursor()
        sql_string = "SELECT data.dateCreated, data.datum, probes.identifier, data.probe_ID FROM data " \
            + " INNER JOIN probes ON data.probe_ID = probes.id WHERE data.event_ID = ?"
        c.execute(sql_string, (a,))
        rows = c.fetchall()
        print('# of rows', len(rows))

        #get the probes for this data set
        probesInSet=[]
        for row in rows:
            if row[3] not in probesInSet:
                probesInSet.append(row[3])
        print('probes in this set: ', probesInSet)
        p = int(input("Which probe data would you like to export? "))
        fname=input("What do you want to call this file? ")



        # setup csv
        with open(fname, 'w', newline='') as csvfile:
            fieldnames = ['probe name','date','temperature']
            writer = csv.DictWriter(csvfile, dialect="excel", fieldnames=fieldnames)

            # Write data
            writer.writeheader()
            for row in rows:
                if row[3] == p:
                    writer.writerow({'probe name':row[2],'date':row[0],'temperature':row[1]})

    def ij(self):
        if not self.db_open:
            DB.open(self)

        c = self.db.cursor()
        sql_string = "SELECT data.dateCreated, data.datum, probes.identifier FROM data" \
            + " INNER JOIN probes ON data.probe_ID = probes.ID WHERE event_ID = 1 and probe_ID=2"
        c.execute(sql_string)
        rows = c.fetchall()
        for row in rows:
            print(row)

    def change_probe_name(self):
        if not self.db_open:
            DB.open(self)

        print("List of Probes")
        DB.list_all_probes(self)
        probe_id = int(input("Which probe do you want to change? "))
        probe_name=input("What do you want to change the probe name to ?")

        asql = "UPDATE {t} SET {n} = ?, {d} = ? WHERE {id} = ?".format(t='probes', d='dateModified', n='name', id='id')
        current_time=dt.now()
        c=self.db.cursor()
        c.execute(asql,(probe_name, current_time, probe_id))
        self.db.commit()
