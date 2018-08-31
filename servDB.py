# file used by server to update values for flask web
import sqlite3
from datetime import datetime as dt
import sys


#  create a database object to handle all tasks

class DB:

    def __init__(self, db_name=""):
        self.db_name = "servDB.sqlite"
        self.db_open = False
        self.db = None

    def open(self):
        self.db = sqlite3.connect(self.db_name)
        self.db_open = True

    def close(self):
        if self.db_open:
            self.db.close()
            self.db_open = False

    def addDevice(self, deviceID, deviceName):
        # open DB
        if not self.db_open:
            DB.open(self)

        # get the current time
        now = dt.now()
        sqlString = "INSERT INTO Devices (deviceId, deviceName, dateCreated, dateModified) \
                    VALUES (?, ?, ?, ?)"
        c = self.db.cursor()
        try:
            c.execute(sqlString, (deviceID, deviceName, now, now))
            self.db.commit()
            return True

        except:
            print("Exception Issued:", sys.exc_info()[0])
            return False

    def addDevicePrompt(self):
        # use prompts to get the device information
        deviceID = input("What is the device id? ")
        deviceName = input("What is the device name? ")

        # save the data
        try:
            if DB.addDevice(self, deviceID, deviceName):
                print("data saved")
            else:
                print("data not saved")
        except:
            print("Exception Issued:", sys.exc_info()[0])

    def listAllDevices(self):
        # open DB
        if not self.db_open:
            DB.open(self)

        c = self.db.cursor()
        sqlString = "SELECT * FROM Devices"
        c.execute(sqlString)
        rows = c.fetchall()
        print("# of rows", len(rows))
        for row in rows:
            print(row)

    def listAllsvIOTValues(self):
        # open DB
        if not self.db_open:
            DB.open(self)

        c = self.db.cursor()
        sqlString = "SELECT * FROM svIOT"
        c.execute(sqlString)
        rows = c.fetchall()
        print("# of rows", len(rows))
        for row in rows:
            print(row)

    def updatesvIOT(self, svIOTID, paramValue):
        # open DB
        if not self.db_open:
            DB.open(self)

        sqlString = "UPDATE svIOT SET paramValue = ?, dateModified = ? 
                    WHERE id = ?"
        now = dt.now()
        c = self.db.cursor()
        try:
            c.execute(sqlString, (paramValue, now, svIOTID)) 
            print("Database update")
            return True
        except:
            print("Exception occured", sys.exc_info()[0])
            return False
            
