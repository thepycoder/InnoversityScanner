import mysql.connector
import time


class DatabaseHandler:

    def __init__(self, user, password, host, database):
        self.cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
        self.cur = self.cnx.cursor()

    def addVisit(self, card, location):

        self.cur.execute("SELECT * FROM current WHERE card = '%s'" % card)
        data = self.cur.fetchone()

        print data

        if not data:
            self.cur.execute("INSERT INTO current (card, location, timestamp) VALUES ('%s', '%s', '%s')" % (card, location, time.strftime('%Y-%m-%d %H:%M:%S')))
        else:
            self.cur.execute("INSERT INTO history (card, inTime, outTime, location) VALUES ('%s', '%s', '%s', '%s')" % (card, data[2], time.strftime('%Y-%m-%d %H:%M:%S'), data[1]))
            self.cur.execute("DELETE FROM current WHERE card = '%s'" % card)

        self.cnx.commit()