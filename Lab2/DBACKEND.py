import psycopg2
import psycopg2.extras
from psycopg2 import ProgrammingError
import csv
from time import gmtime, strftime


class Database():
    def __init__(self):
        self.connection = psycopg2.connect("host=host, dbname=postgres")
        self.connection.autocommit=True
        self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def create_tables(self):
        self.cursor.execute("CREATE TABLE people(userid integer PRIMARY KEY, name varchar, position varchar, companyid varchar, teamid varchar, password varchar);")
        self.cursor.execute("CREATE TABLE team (teamid varchar, name varchar, description varchar, active varchar, PRIMARY KEY(teamid));")
        self.cursor.execute("CREATE TABLE participations(bookingid varchar, userid integer, PRIMARY KEY(bookingid, userid));")
        self.cursor.execute("CREATE TABLE rooms(roomid varchar PRIMARY KEY, name varchar, price integer, floor integer, capacity integer);")
        self.cursor.execute("CREATE TABLE bookings(bookingid integer PRIMARY KEY, start_time TIMESTAMP , end_time TIMESTAMP, roomid varchar, userid varchar, teamid varchar);")
        self.cursor.execute("CREATE TABLE companies(id varchar PRIMARY KEY, name varchar, description varchar, country varchar);")

    def clear_tables(self):
        tableList = ['people', 'team', 'participations', 'rooms', 'bookings', 'companies']
        for table in tableList:
            try:
                self.cursor.execute("DROP TABLE "+table)
            except ProgrammingError:
                pass

    def do_nothing(self):
        pass

    def dummydata(self):
        users=readdata('users.csv')
        for user in users:
            self.cursor.execute("INSERT INTO people(userid, name, position, companyid, teamid, password) VALUES (%s, %s, %s, %s, %s, %s)", (user[0].strip('\ufeff'), user[1],user[2],user[3],user[4],user[5]))

        rooms=readdata('rooms.csv')
        for room in rooms:
            self.cursor.execute("INSERT INTO rooms(roomid, name, price, floor, capacity) VALUES (%s, %s, %s, %s, %s)", (room[0].strip('\ufeff'), room[1], room[2], room[3], room[4]))

        bookings=readdata('bookings.csv')
        for booking in bookings:
            self.cursor.execute("INSERT INTO bookings(bookingid,start_time, end_time, roomid, userid, teamid) VALUES (%s, %s, %s, %s, %s, %s)", (booking[0].strip('\ufeff'), booking[1], booking[2], booking[3], booking[4], booking[5]))

        companies=readdata('companies.csv')
        for company in companies:
            self.cursor.execute("INSERT INTO companies(id, name, description, country) VALUES (%s, %s, %s, %s)", (company[0].strip('\ufeff'), company[1], company[2], company[3]))

        teams=readdata('team.csv')
        for team in teams:
            self.cursor.execute("INSERT INTO team(teamid, name, description, active) VALUES (%s, %s, %s, %s)", (team[0].strip('\ufeff'), team[1], team[2], team[3]))

        partici = readdata('participations.csv')
        for par in partici:
            self.cursor.execute("INSERT INTO participations(bookingid, userid) VALUES (%s, %s)", (par[0].strip('\ufeff'), par[1]))



    def insert_entry(self, table, attributes, data):
        if table == 'team':
            self.insert_team_entry(table, attributes, data)
        if table == 'bookings':
            self.insert_booking(data, attributes)
        else:
            s='%s'
            length=len(attributes)
            if length==len(data):
                    for i in range(0, length-1):
                        s=s+', %s'
                    att=', '.join(attributes)
                    query= ("INSERT INTO "+table+"("+att+") VALUES("+s+");")
                    self.cursor.execute(query, data)

    def insert_booking(self, data, attributes):
        result=self.check_if_booked(data[3],data[1],data[2])
        if (result==True):
            teamid=self.get_teamid(data[4])
            s = '%s'
            length = len(attributes)
            if length == len(data):
                for i in range(0, length - 1):
                    s = s + ', %s'
                att = ', '.join(attributes)
                query1 = ("INSERT INTO bookings(" + att + ") VALUES(" + s + ");")
                self.cursor.execute(query1, data)
                self.cursor


    def insert_team_entry(self, table, attributes, data):
        s='%s'
        length=len(attributes)
        if length==len(data):
                for i in range(0, length-1):
                    s=s+', %s'
                att=', '.join(attributes)
                query1= ("INSERT INTO "+table+"("+att+") VALUES("+s+");")
                query2= ("INSERT INTO allteam("+att+") VALUES("+s+");")
                self.cursor.execute(query1, data)
                self.cursor.execute(query2, data)

    def delete_entry(self, table, primkey, id):
        query="DELETE FROM "+table+" WHERE "+primkey+"='"+id+"'"
        self.cursor.execute(query)

    def delete_entry2(self, table, primkey1, primkey2, id1, id2):
        query="DELETE FROM "+table+" WHERE "+primkey1+"='"+id1+"' and "+primkey2+"='"+id2+"'"
        self.cursor.execute(query)

    def delete_team_entry(self, table, primkey1, primkey2, id1, id2):
        query="DELETE FROM "+table+" WHERE "+primkey1+"='"+id1+"' and "+primkey2+"='"+id2+"'"
        self.cursor.execute(query)

    def change_entry(self, table, primkey, id, attributes, newvalues):
        newdata=(attributes[0]+"='"+newvalues[0]+"'")
        length=len(attributes)
        for i in range(1, length):
            newdata=(newdata+", "+attributes[i]+"='"+newvalues[i]+"'")
        query = ("UPDATE "+table+" SET "+newdata+" WHERE "+primkey+"='"+id+"'")
        self.cursor.execute(query)

    def change_team_entry(self, table, primkey, id, attributes, newvalues):
        newdata = (attributes[0] + "='" + newvalues[0] + "'")
        length = len(attributes)
        for i in range(1, length):
            newdata = (newdata + ", " + attributes[i] + "='" + newvalues[i] + "'")
        query1 = ("UPDATE " + table + " SET " + newdata + " WHERE " + primkey + "='" + id + "'")
        query2 = ("UPDATE allteam SET " + newdata + " WHERE " + primkey + "='" + id + "'")
        self.cursor.execute(query)

    def display_rooms(self, date):
        query="SELECT * FROM BOOKINGS WHERE DATE='"+date+"'"
        self.cursor.execute(query)
        bookings=self.cursor.fetchall()
        """for booking in bookings:
            print("Room: %s\tStart: %s\tEnd: %s"% (booking['roomid'], booking['start_time'], booking['end_time']))
            print("———————————————————————————")"""
        return bookings

    def key_is_ok(self, table, attribute, testkey):
        query="SELECT 'Occupied' FROM "+table+" WHERE "+attribute+"='"+testkey+"'"
        self.cursor.execute(query)
        try:
            result=self.cursor.fetchone()
            if result[0]=='':
                return False
            else:
                return False
        except:
            return True

    def check_if_booked(self, room, start, stop):
        query="WITH CTE(start, stop) AS (SELECT start_time, end_time FROM bookings WHERE roomid = '"+room+"') SELECT start, stop,CASE WHEN '"+start+"'<'"+stop+"' AND (('"+stop+"'<= Cte.start) OR ('"+start+"' >= cte.stop)) THEN 'Free' ELSE 'Booked' END FROM CTE"
        self.cursor.execute(query)
        list=self.cursor.fetchall()
        for booking in list:
            if booking[2]=='Booked':
                return False
        return True
    def show1attribute(self, table, attribute):
        query = "SELECT DISTINCT " + attribute + " FROM " +table+ " ORDER BY " + attribute
        self.cursor.execute(query)
        B = []
        A = self.cursor.fetchall()
        for row in A:
            B.append(row[0])
        return B

    def get_teamid(self, id):
        query="SELECT teamid FROM people WHERE userid='"+id+"'"
        self.cursor.execute(query)
        id=self.cursor.fetchone()
        return id[0]

    def getTeamID(self, useridX):
        query = "SELECT teamid FROM people WHERE people.userid = "+useridX
        self.cursor.execute(query)
        A = self.cursor.fetchone()
        for row in A:
            return row

    def showLastID(self, table, primkey):
        query="SELECT "+primkey+" FROM "+table+" ORDER BY "+primkey+" DESC"
        self.cursor.execute(query)
        A = self.cursor.fetchone()
        for row in A:
           return row

    def groups_debit(self):
        date=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        list = [
            "WITH cte(teamid, tid, price) AS (SELECT teamid, DATE_PART('hour', end_time::TIME - start_time::time) * 60 + DATE_PART('minute', end_time::TIME - start_time::time), price FROM bookings INNER JOIN rooms ON rooms.roomid=bookings.roomid WHERE bookings.start_time < '",
            date, "') SELECT teamid, sum(tid*price/60) AS debit FROM cte GROUP BY teamid ORDER BY teamid"]
        query="".join(list)
        self.cursor.execute(query)
        teams=self.cursor.fetchall()
        for t in teams:
            print("Team nr and total costs: "+str(t))
        return teams

    def show_available_rooms(self, date):
        query = "SELECT * FROM roomid"
        self.cursor.execute(query)

    def delete_booking(self,userid, bookingid1):
        date=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        query="SELECT COALESCE((SELECT userid FROM bookings WHERE bookingid = "+bookingid1+" AND start_time > '"+date+"'), 'No match')"
        self.cursor.execute(query)
        result=self.cursor.fetchone()[0]
        if result!='No match':
            if userid==result:
                self.delete_entry('bookings', 'bookingid', bookingid1)
                print('Booking has been deleted')
            else:
                #------" Delete Requsted 0->1 "--------
                print(userid)
                print(result)
                print('The one making the booking needs to delete the booking')
        else:
            print(bookingid1)
            print('No match or can not be unbooked')
            print(result)

    def costs_for_period(self,start,end):
        query="WITH cte AS (SELECT teamid,roomid, (DATE_PART('hour', end_time::TIME - start_time::time) * 60 + DATE_PART('minute', end_time::TIME - start_time::time))/60 AS TIME FROM bookings WHERE '"+start+"' < '"+end+"' AND (('"+start+"'<= start_time) and ('"+end+"' >= end_time))), cte1 AS ( SELECT teamid, sum(cte.time*rooms.price) AS debit FROM rooms INNER JOIN cte ON cte.roomid=rooms.roomid GROUP BY teamid ORDER BY debit DESC) SELECT * FROM cte1"
        self.cursor.execute(query)
        teams=self.cursor.fetchall()
        for team in teams:
            team[1]=str(team[1])
        return teams

    def showtable(self,table):
        if table=='team':
            return self.showTeams()
        else:
         query="SELECT * FROM "+table+" ORDER BY 1 ASC"
         self.cursor.execute(query)
         return self.cursor.fetchall()
    def showTeams(self):
        query="SELECT * FROM team where active='Yes'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete(self, table, primkey, id):
        query="DELETE FROM "+table+" WHERE "+primkey+"='"+id+"'"
        self.cursor.execute(query)

    def delete_team(self, primkey, id):
        newdata = "active = 'No'"
        query=("UPDATE team SET "+newdata+" WHERE "+primkey+"='"+id+"'")
        self.cursor.execute(query)

    def show_bookings_for_date(self, date):
        query = "SELECT roomid FROM rooms ORDER BY roomid"
        self.cursor.execute(query)
        roomids = self.cursor.fetchall()
        height = len(roomids)
        list = [
            "WITH cte AS (SELECT roomid, START_time, END_time, DATE_PART('hour', end_time::TIME - start_time::time) * 60 + DATE_PART('minute', end_time::TIME - start_time::time) AS length FROM bookings WHERE STARt_time BETWEEN '",
            date, " 00:00:00' AND '", date, " 23:59:59') SELECT roomid, START_time, length/60 AS length FROM cte"]
        query = ''.join(list)
        self.cursor.execute(query)
        bookings = self.cursor.fetchall()
        time = ['00:00:00', '01:00:00', '02:00:00', '03:00:00', '04:00:00', '05:00:00', '06:00:00', '07:00:00',
                '08:00:00', '09:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00',
                '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00', '23:00:00', '24:00:00']
        A = [[0 for x in range(len(time))] for y in range(height)]
        for i in range(0, height):
            A[i][0] = roomids[i][0]
            for j in range(1, len(time)):
                A[i][j] = '-free-'
        for booking in bookings:
            bookingdate = str(booking[1])
            bookingdate = bookingdate[:10]
            if date == bookingdate:
                for i in range(0, height):
                    if A[i][0] == booking[0]:
                        starttime = str(booking[1])
                        starttime = starttime[11:]
                        for tid in time:
                            if starttime == tid:
                                start = int(tid[:2]) + 1
                                bookinglength = int(booking[2])
                                for j in range(start, start + bookinglength):
                                    A[i][j] = 'Booked'
        return A

    def booking_ok(self, date):
        pass

#————————————————————————————————————————————————————————————————————————————
#--- Input for the different functions
def readdata(filename):
    list=[]
    with open(filename, newline='',encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            list.append(row)
        return list
#--Checks if entered userid and password matches entry in database
def login(d,userid, passwordattempt):
    d.cursor.execute("SELECT * FROM people WHERE userid=%s;", [userid])
    user=d.cursor.fetchall()
    if user != []:
        u = user[0]
        if passwordattempt==u['password']:
            print("Welcome %s" % u['name'])
            return True, u
        else:
            print("Wrong userid or password")
            return False, []
    else:
        print("No userid for %s" % userid)
        return False, []
#-- Loops until correct userid and password has been entered, returns the user which is logged in
def verification(d):
    while True:
        id = str(input('Enter userid: '))
        passatempt = str(input('Enter password: '))
        access, user = login(d,id, passatempt)
        if access:
            return user

def main():
     A=Database()
     A.clear_tables()
     A.create_tables()
     A.dummydata()
     print(A.check_if_booked('605', '2018-02-26 07:00:00', '2018-02-26 09:00:00'))
     A.delete_booking('122622', '112010')
     teams=A.costs_for_period('2018-03-05 00:00:00','2018-03-05 23:59:59')
     for team in teams:
         print(team)
     A.insert_entry('bookings', ['bookingid','start_time','end_time','roomid', 'userid','teamid'], ['0','2018-05-01 08:00:00','2018-05-01 16:00:00','605', '122614'])

main()
