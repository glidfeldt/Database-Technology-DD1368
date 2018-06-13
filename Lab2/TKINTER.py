# STATEMENTS ----------------------
# The code for changing pages was derived from:
# http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

# IMPORTS -------------------------
import tkinter as tk
from DBBACKEND import *
import tkinter.ttk as ttk
import tkinter as Tkinter
import datetime

# CONSTANTS -----------------------
LARGE_FONT = ("Verdana", 12)
#Table headers
peopleHeader = ['UserID', 'name', 'position', 'companyid', 'teamid', 'password']
teamHeader = ['TeamID', 'name', 'Description']
participationsHeader = ['UserID', 'BookingID']
roomsHeader = ['RoomID', 'name', 'price', 'floor', 'capacity']
bookingsHeader2 = ['bookingid','start_time', 'end_time', 'roomid', 'userid', 'teamid']
bookingsHeader = ['BookingID', 'date', 'start_time', 'end_time', 'RoomID', 'UserID', 'TeamID']
companiesHeader = ['id', 'name', 'description', 'country']
costsHeader = ['TeamID', 'Total Costs']

# ClASSES -------------------------
class MeetifyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top")#, fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("Meetify - a meeting booking system")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config(background="gray")
        self.d = Database()
        self.d.clear_tables()
        self.d.create_tables()
        self.d.dummydata()
        self.loggedInUser = None

        self.frames = {}

        for X in (LoginPage, MainMenu, UserWindow, CompaniesWindow, TeamsWindow, ParticipantWindow, BookingsWindow, RoomsWindow, CostsWindow):
            frame = X(container, self)

            self.frames[X] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def login(self, userid, pwAttempt):
        self.d.cursor.execute("SELECT * FROM people WHERE userid=%s;", [userid])
        row = self.d.cursor.fetchall()
        if row != []:
            u = row[0]
            if pwAttempt == u['password']:
                self.loggedInUser = u['userid']
                self.show_frame(MainMenu)

            else:
                return False
        else:
            return False

    def returnLoggedInUser(self):
        if self.loggedInUser != None:
            return self.loggedInUser
        else:
            print('No logged in user.')

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headLabel = tk.Label(self, text="                        M E E T I F Y                        ", bg="grey")
        headLabel.configure(font=("Helvetica", 40, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=2, sticky="NSEW")

        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________",
                             bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=2, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        usrLabel = tk.Label(self, text="User name")
        usrLabel.grid(row=3, column=5, sticky="e")
        usrEntry = tk.Entry(self)
        usrEntry.grid(row=3, column=6, sticky="W")

        pwLabel = tk.Label(self, text="Password")
        pwLabel.grid(row=4, column=5, sticky="e")
        pwEntry = tk.Entry(self)
        pwEntry.grid(row=4, column=6, sticky="W")

        loginBtn = tk.Button(self, text="Login",
                             command=lambda: controller.login(usrEntry.get(), pwEntry.get()))
        loginBtn.grid(row=5, column=5, sticky="E")

        #TEMP - TAKE AWAY!!!!
        mainMenu = tk.Button(self, text="Cheat into Main Menu", bg="grey",
                             command=lambda: controller.show_frame(MainMenu))
        mainMenu.grid(row=5, column=6, sticky="W")

class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headLabel = tk.Label(self, text="MAIN MENU", bg="grey")
        headLabel.configure(font=("Helvetica", 20, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=1, sticky="NWSE")
        self.app = controller
        app = self.app

        A = controller.d.do_nothing()

        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=1, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        headLabel.grid_rowconfigure(0, weight=1)
        headLabel.grid_columnconfigure(0, weight=1)

        logout = tk.Button(self, text="Log out", bg="grey",
                           command=lambda: controller.show_frame(LoginPage))
        logout.grid(row=0, column=10, sticky="E")


        usrLabel = tk.Label(self, text="Users")
        usrLabel.grid(row=3, column=1, columnspan=2, sticky="E")
        usrbutton = tk.Button(self, text="View or edit",
                            command=lambda: controller.show_frame(UserWindow))
        usrbutton.grid(row=3, column=3)

        compLabel = tk.Label(self, text="Companies")
        compLabel.grid(row=4, column=1, columnspan=2, sticky="E")
        compbutton = tk.Button(self, text="View or edit",
                            command=lambda: controller.show_frame(CompaniesWindow))
        compbutton.grid(row=4, column=3)

        teamLabel = tk.Label(self, text="Teams")
        teamLabel.grid(row=5, column=1, columnspan=2, sticky="E")
        teambutton = tk.Button(self, text="View or edit",
                            command=lambda: controller.show_frame(TeamsWindow))
        teambutton.grid(row=5, column=3)

        participationsLabel = tk.Label(self, text="Participants")
        participationsLabel.grid(row=6, column=1, columnspan=2, sticky="E")
        participationsbutton = tk.Button(self, text="View or edit",
                               command=lambda: controller.show_frame(ParticipantWindow))
        participationsbutton.grid(row=6, column=3)

        bookingLabel = tk.Label(self, text="Bookings")
        bookingLabel.grid(row=7, column=1, columnspan=2, sticky="E")
        bookingbutton = tk.Button(self, text="View or edit",
                            command=lambda: controller.show_frame(BookingsWindow))
        bookingbutton.grid(row=7, column=3)

        roomLabel = tk.Label(self, text="Rooms")
        roomLabel.grid(row=8, column=1, columnspan=2, sticky="E")
        roombutton = tk.Button(self, text="View or edit",
                            command=lambda: controller.show_frame(RoomsWindow))
        roombutton.grid(row=8, column=3)

        costLabel = tk.Label(self, text="Costs")
        costLabel.grid(row=9, column=1, columnspan=2, sticky="E")
        costbutton = tk.Button(self, text="View or edit",
                            command=lambda: controller.show_frame(CostsWindow))
        costbutton.grid(row=9, column=3)

        line2Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        line2Label.configure(font=("Helvetica", 20, "bold"))
        line2Label.grid(row=10, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        #DATE CHOOZZZZZER

        dateLabel = tk.Label(self, text="View bookings & availability")
        dateLabel.grid(row=11, column=4, sticky="E")

        base1 = datetime.date.today()
        date_list1 = [base1 - datetime.timedelta(days=x) for x in range(0, 30)]
        date_list2 = [base1 + datetime.timedelta(days=x) for x in range(1, 30)]
        date_list1.reverse()
        for elem in date_list2:
            date_list1.append(elem)
        self.date_variable1 = tk.StringVar(self)
        self.date_variable1.set(datetime.date.today())  # default value
        self.w1 = tk.OptionMenu(self, self.date_variable1, *date_list1)
        self.w1.grid(row=11, column=5, sticky="W")

        pastButton = tk.Button(self, text="View date",
                               command=lambda: self.show_bookings(str(self.date_variable1.get())))
        pastButton.grid(row=11, column=5, sticky="E")

        line3Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________",
                              bg="grey")
        line3Label.configure(font=("Helvetica", 20, "bold"))
        line3Label.grid(row=12, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        columnList = (
        '0', '1', '2', '3', '4', '5', '6', '8', '9', '10', '11', '12',
        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24')
        self.tree = tk.ttk.Treeview(self, columns=columnList)
        self.tree.heading('#0', text="Meeting Room")
        self.tree.heading('#1', text="00-01")
        self.tree.heading('#2', text="01-02")
        self.tree.heading('#3', text="02-03")
        self.tree.heading('#4', text="03-04")
        self.tree.heading('#5', text="04-05")
        self.tree.heading('#6', text="05-06")
        self.tree.heading('#7', text="06-07")
        self.tree.heading('#8', text="07-08")
        self.tree.heading('#9', text="08-09")
        self.tree.heading('#10', text="09-10")
        self.tree.heading('#11', text="10-11")
        self.tree.heading('#12', text="11-12")
        self.tree.heading('#13', text="12-13")
        self.tree.heading('#14', text="13-14")
        self.tree.heading('#15', text="14-15")
        self.tree.heading('#16', text="15-16")
        self.tree.heading('#17', text="16-17")
        self.tree.heading('#18', text="17-18")
        self.tree.heading('#19', text="18-19")
        self.tree.heading('#20', text="19-20")
        self.tree.heading('#21', text="20-21")
        self.tree.heading('#22', text="21-22")
        self.tree.heading('#23', text="22-23")
        self.tree.heading('#24', text="23-24")
        self.tree.grid(row=13, rowspan=20, columnspan=11, sticky='nsew')
        self.treeview = self.tree
        self.treeview.column('0', width=50)
        for column in columnList:
            self.treeview.column(column, width=50)


        for t in self.treeview.get_children():
            self.treeview.delete(t)
        A = controller.d.show_bookings_for_date(str(datetime.date.today()))
        for booking in A:
            self.treeview.insert('', 'end', text=booking[0], values=(
            booking[1], booking[2], booking[3], booking[4], booking[5], booking[6], booking[7], booking[8], booking[9],
            booking[10], booking[11], booking[12], booking[13], booking[14], booking[15], booking[16], booking[17],
            booking[18], booking[19], booking[20], booking[21], booking[22], booking[23], booking[24]))

    def show_bookings(self, date=str(datetime.date.today())):
        print(str(self.date_variable1.get()))
        print("hej")
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        A = self.app.d.show_bookings_for_date(date)
        for booking in A:
            self.treeview.insert('', 'end', text=booking[0], values=(
            booking[1], booking[2], booking[3], booking[4], booking[5], booking[6], booking[7], booking[8],booking[9],
            booking[10], booking[11], booking[12], booking[13], booking[14], booking[15], booking[16], booking[17],
            booking[18], booking[19], booking[20], booking[21], booking[22], booking[23], booking[24]))

class UserWindow(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        headLabel = tk.Label(self, text="VIEW & EDIT USERS", bg="grey")
        headLabel.configure(font=("Helvetica", 20, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=1, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        headLabel.grid_rowconfigure(0, weight=1)
        headLabel.grid_columnconfigure(0, weight=1)

        logout = tk.Button(self, text="  Log out      ", bg="grey",command=lambda: controller.show_frame(LoginPage))
        logout.grid(row=0, column=10, sticky="E")
        mainMenu = tk.Button(self, text="  Main Menu        ", bg="grey",command=lambda: controller.show_frame(MainMenu))
        mainMenu.grid(row=0, column=9, sticky="E")

        header = peopleHeader
        self.attrLabel1 = tk.Label(self, text=header[0])
        self.attrLabel1.grid(row=3, column=2)
        self.attrLabel2 = tk.Label(self, text=header[1])
        self.attrLabel2.grid(row=3, column=3)
        self.attrLabel3 = tk.Label(self, text=header[2])
        self.attrLabel3.grid(row=3, column=4)
        self.attrLabel4 = tk.Label(self, text=header[3])
        self.attrLabel4.grid(row=3, column=5)
        self.attrLabel5 = tk.Label(self, text=header[4])
        self.attrLabel5.grid(row=3, column=6)
        self.attrLabel6 = tk.Label(self, text=header[5])
        self.attrLabel6.grid(row=3, column=7)

        self.addLabel = tk.Label(self, text="Add")
        self.addLabel.grid(row=4, column=1, sticky="E")
        self.addEntry1 = tk.Entry(self)
        self.addEntry1.grid(row=4, column=2)
        self.addEntry2 = tk.Entry(self)
        self.addEntry2.grid(row=4, column=3)
        self.addEntry3 = tk.Entry(self)
        self.addEntry3.grid(row=4, column=4)
        self.addEntry4 = tk.Entry(self)
        self.addEntry4.grid(row=4, column=5)
        self.addEntry5 = tk.Entry(self)
        self.addEntry5.grid(row=4, column=6)
        self.addEntry6 = tk.Entry(self)
        self.addEntry6.grid(row=4, column=7)

        self.addbutton = tk.Button(self, text="Add", command = self.insert_data)
        self.addbutton.grid(row=4, column=9)
        self.editLabel = tk.Label(self, text="Edit")
        self.editLabel.grid(row=5, column=1, sticky="E")
        self.editEntryPrimkey = tk.Entry(self)
        self.editEntryPrimkey.grid(row=5, column=2)
        self.editEntry2 = tk.Entry(self)
        self.editEntry2.grid(row=5, column=3)
        self.editEntry3 = tk.Entry(self)
        self.editEntry3.grid(row=5, column=4)
        self.editEntry4 = tk.Entry(self)
        self.editEntry4.grid(row=5, column=5)
        self.editEntry5 = tk.Entry(self)
        self.editEntry5.grid(row=5, column=6)
        self.editEntry6 = tk.Entry(self)
        self.editEntry6.grid(row=5, column=7)

        self.editbutton = tk.Button(self, text="Edit", command=self.edit_data)
        self.editbutton.grid(row=5, column=9)
        self.deleteLabel = tk.Label(self, text="Delete")
        self.deleteLabel.grid(row=6, column=1, sticky="E")
        self.deleteEntry = tk.Entry(self)
        self.deleteEntry.grid(row=6, column=2)
        self.deletebutton = tk.Button(self, text="Delete", command=self.delete_data)
        self.deletebutton.grid(row=6, column=9)
        self.line2Label = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________",
                             bg="grey")
        self.line2Label.configure(font=("Helvetica", 20, "bold"))
        self.line2Label.grid(row=7, column=1, columnspan=11, rowspan=1, sticky="NWSE")


        self.tree = tk.ttk.Treeview(self, columns=('0', '1', '2', '3', '4', '5'))
        self.tree.heading('#0', text=header[0])
        self.tree.heading('#1', text=header[1])
        self.tree.heading('#2', text=header[2])
        self.tree.heading('#3', text=header[3])
        self.tree.heading('#4', text=header[4])
        self.tree.heading('#5', text=header[5])
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.column('#1', stretch=Tkinter.YES)
        self.tree.column('#2', stretch=Tkinter.YES)
        self.tree.column('#3', stretch=Tkinter.YES)
        self.tree.column('#4', stretch=Tkinter.YES)
        self.tree.column('#5', stretch=Tkinter.YES)
        self.tree.grid(row=10, rowspan=20, columnspan=11, sticky='nsew')
        self.treeview = self.tree

        line3Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________",
                              bg="grey")
        line3Label.configure(font=("Helvetica", 20, "bold"))
        line3Label.grid(row=41, column=1, columnspan=11, rowspan=1, sticky="NWSE")
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        A=controller.d.showtable('people')
        for user in A:
            self.treeview.insert('', 'end', text=user[0], values=(user[1], user[2], user[3], user[4], user[5]))

    def insert_data(self):
        attributes=peopleHeader
        id = self.addEntry1.get()
        if app.d.key_is_ok('people', 'userid', id):
            data=[id,self.addEntry2.get(), self.addEntry3.get(), self.addEntry4.get(), self.addEntry5.get(), self.addEntry6.get()]
            table='people'
            primkey='userid'
            app.d.insert_entry(table, attributes, data)
            self.treeview.insert('', 'end', text=self.addEntry1.get(), values=(self.addEntry2.get(), self.addEntry3.get(), self.addEntry4.get(), self.addEntry5.get()))
            A = app.d.showtable('people')
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            for record in A:
                self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3], record[4], record[5]))

    def edit_data(self):
        id=self.editEntryPrimkey.get()
        if id != '':
            attributes=[]
            data=[]
            name=self.editEntry2.get()
            if name!='':
                attributes.append('name')
                data.append(name)
            email=self.editEntry3.get()
            if email!='':
                attributes.append('position')
                data.append(email)
            compid=self.editEntry4.get()
            if compid!='':
                attributes.append('companyid')
                data.append(compid)
            team=self.editEntry5.get()
            if team!='':
                attributes.append('teamid')
                data.append(team)
            pw=self.editEntry6.get()
            if pw != '':
                attributes.append('password')
                data.append(pw)
            table = 'people'
            primkey = 'userid'
            app.d.change_entry(table, primkey,id,attributes,data)
            A=app.d.showtable('people')
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            for record in A:
                self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3], record[4], record[5]))

    def delete_data(self):
        table = "people"
        primkey = "userid"
        id = self.deleteEntry.get()
        app.d.delete_entry(table,primkey,id)
        A = app.d.showtable('people')
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        for record in A:
            self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3], record[4], record[5]))

class CompaniesWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headLabel = tk.Label(self, text="VIEW & EDIT COMAPIES", bg="grey")
        headLabel.configure(font=("Helvetica", 20, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=1, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        headLabel.grid_rowconfigure(0, weight=1)
        headLabel.grid_columnconfigure(0, weight=1)

        logout = tk.Button(self, text="  Log out      ", bg="grey",command=lambda: controller.show_frame(LoginPage))
        logout.grid(row=0, column=10, sticky="E")
        mainMenu = tk.Button(self, text="  Main Menu        ", bg="grey",command=lambda: controller.show_frame(MainMenu))
        mainMenu.grid(row=0, column=9, sticky="E")

        header = companiesHeader
        self.attrLabel1 = tk.Label(self, text=header[0])
        self.attrLabel1.grid(row=3, column=2)
        self.attrLabel2 = tk.Label(self, text=header[1])
        self.attrLabel2.grid(row=3, column=3)
        self.attrLabel3 = tk.Label(self, text=header[2])
        self.attrLabel3.grid(row=3, column=4)
        self.attrLabel4 = tk.Label(self, text=header[3])
        self.attrLabel4.grid(row=3, column=5)


        self.addLabel = tk.Label(self, text="Add")
        self.addLabel.grid(row=4, column=1, sticky="E")
        self.addEntry1 = tk.Entry(self)
        self.addEntry1.grid(row=4, column=2)
        self.addEntry2 = tk.Entry(self)
        self.addEntry2.grid(row=4, column=3)
        self.addEntry3 = tk.Entry(self)
        self.addEntry3.grid(row=4, column=4)
        self.addEntry4 = tk.Entry(self)
        self.addEntry4.grid(row=4, column=5)


        self.addbutton = tk.Button(self, text="Add", command=self.insert_data)
        self.addbutton.grid(row=4, column=9)

        self.editLabel = tk.Label(self, text="Edit")
        self.editLabel.grid(row=5, column=1, sticky="E")
        self.editEntryPrimkey = tk.Entry(self)
        self.editEntryPrimkey.grid(row=5, column=2)
        self.editEntry2 = tk.Entry(self)
        self.editEntry2.grid(row=5, column=3)
        self.editEntry3 = tk.Entry(self)
        self.editEntry3.grid(row=5, column=4)
        self.editEntry4 = tk.Entry(self)
        self.editEntry4.grid(row=5, column=5)


        self.editbutton = tk.Button(self, text="Edit", command=self.edit_data)
        self.editbutton.grid(row=5, column=9)

        self.deleteLabel = tk.Label(self, text="Delete")
        self.deleteLabel.grid(row=6, column=1, sticky="E")

        self.deleteEntry = tk.Entry(self)
        self.deleteEntry.grid(row=6, column=2)

        self.deletebutton = tk.Button(self, text="Delete", command=self.delete_data)
        self.deletebutton.grid(row=6, column=9)

        self.line2Label = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________",
                             bg="grey")
        self.line2Label.configure(font=("Helvetica", 20, "bold"))
        self.line2Label.grid(row=7, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        self.tree = tk.ttk.Treeview(self, columns=('1', '2', '3'))
        self.tree.heading('#0', text=header[0])
        self.tree.heading('#1', text=header[1])
        self.tree.heading('#2', text=header[2])
        self.tree.heading('#3', text=header[3])
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.column('#1', stretch=Tkinter.YES)
        self.tree.column('#2', stretch=Tkinter.YES)
        self.tree.column('#3', stretch=Tkinter.YES)

        self.tree.grid(row=10, rowspan=20, columnspan=11, sticky='nsew')
        self.treeview = self.tree

        line3Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________",
                              bg="grey")
        line3Label.configure(font=("Helvetica", 20, "bold"))
        line3Label.grid(row=41, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        A = controller.d.showtable('companies')

        for user in A:
            self.treeview.insert('', 'end', text=user[0], values=(user[1], user[2], user[3]))

    def insert_data(self):
        attributes = companiesHeader
        id = self.addEntry1.get()
        if app.d.key_is_ok('companies', 'id', id):
            data = [id,self.addEntry2.get(), self.addEntry3.get(), self.addEntry4.get()]
            table = 'companies'
            primkey='id'
            app.d.insert_entry(table, attributes, data)
            self.treeview.insert('', 'end', text=self.addEntry1.get(), values=(self.addEntry2.get(), self.addEntry3.get(), self.addEntry4.get()))
            A = app.d.showtable('companies')
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            for record in A:
                self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3]))

    def edit_data(self):
        id=self.editEntryPrimkey.get()
        if id != '':
            attributes=[]
            data=[]
            name=self.editEntry2.get()
            if name!='':
                attributes.append('name')
                data.append(name)
            description=self.editEntry3.get()
            if description!='':
                attributes.append('description')
                data.append(description)
            country=self.editEntry4.get()
            if country!='':
                attributes.append('country')
                data.append(compid)

            table = 'companies'
            primkey = 'id'
            app.d.change_entry(table, primkey,id,attributes,data)
            A=app.d.showtable('companies')
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            for record in A:
                self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3]))

    def delete_data(self):
        table = "companies"
        primkey = "id"
        id = self.deleteEntry.get()
        app.d.delete_entry(table,primkey,id)
        A = app.d.showtable('companies')
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        for record in A:
            self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3]))

class TeamsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headLabel = tk.Label(self, text="VIEW & EDIT TEAMS", bg="grey")
        headLabel.configure(font=("Helvetica", 20, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=1, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        headLabel.grid_rowconfigure(0, weight=1)
        headLabel.grid_columnconfigure(0, weight=1)

        logout = tk.Button(self, text=" Log out  ", bg="grey",command=lambda: controller.show_frame(LoginPage))
        logout.grid(row=0, column=10, sticky="E")
        mainMenu = tk.Button(self, text=" Main Menu   ", bg="grey",command=lambda: controller.show_frame(MainMenu))
        mainMenu.grid(row=0, column=10, sticky="W")

        header = teamHeader
        self.attrLabel1 = tk.Label(self, text=header[0])
        self.attrLabel1.grid(row=3, column=2)
        self.attrLabel2 = tk.Label(self, text=header[1])
        self.attrLabel2.grid(row=3, column=3)
        self.attrLabel3 = tk.Label(self, text=header[2])
        self.attrLabel3.grid(row=3, column=4)

        self.addLabel = tk.Label(self, text="Add")
        self.addLabel.grid(row=4, column=1, sticky="E")



        self.addEntry2 = tk.Entry(self)
        self.addEntry2.grid(row=4, column=3)
        self.addEntry3 = tk.Entry(self)
        self.addEntry3.grid(row=4, column=4)


        self.addbutton = tk.Button(self, text="Add", command=self.insert_data)
        self.addbutton.grid(row=4, column=9)

        self.editLabel = tk.Label(self, text="Edit")
        self.editLabel.grid(row=5, column=1, sticky="E")
        self.editEntryPrimkey = tk.Entry(self)
        self.editEntryPrimkey.grid(row=5, column=2)
        self.editEntry2 = tk.Entry(self)
        self.editEntry2.grid(row=5, column=3)
        self.editEntry3 = tk.Entry(self)
        self.editEntry3.grid(row=5, column=4)

        self.editbutton = tk.Button(self, text="Edit", command=self.edit_data)
        self.editbutton.grid(row=5, column=9)

        self.deleteLabel = tk.Label(self, text="Delete")
        self.deleteLabel.grid(row=6, column=1, sticky="E")

        self.deleteEntry = tk.Entry(self)
        self.deleteEntry.grid(row=6, column=2)

        self.deletebutton = tk.Button(self, text="Delete", command=self.delete_data)
        self.deletebutton.grid(row=6, column=9)

        self.line2Label = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________",
                             bg="grey")
        self.line2Label.configure(font=("Helvetica", 20, "bold"))
        self.line2Label.grid(row=7, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        self.tree = tk.ttk.Treeview(self, columns=('1', '2'))
        self.tree.heading('#0', text=header[0])
        self.tree.heading('#1', text=header[1])
        self.tree.heading('#2', text=header[2])
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.column('#1', stretch=Tkinter.YES)
        self.tree.column('#2', stretch=Tkinter.YES)

        self.tree.grid(row=10, rowspan=20, columnspan=11, sticky='nsew')
        self.treeview = self.tree

        line3Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________",
                              bg="grey")
        line3Label.configure(font=("Helvetica", 20, "bold"))
        line3Label.grid(row=41, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        A = controller.d.showtable('team')
        for user in A:
            self.treeview.insert('', 'end', text=user[0], values=(user[1], user[2]))

    def insert_data(self):
        attributes = teamHeader
        id = str(int(app.d.showLastID('allteam', 'teamid'))+1)
        if app.d.key_is_ok('team','teamid',id):
            data = [id, self.addEntry2.get(), self.addEntry3.get()]
            table = 'team'
            primkey = 'teamid'
            app.d.insert_team_entry(table, attributes, data)
            self.treeview.insert('', 'end', text=id, values=(
            self.addEntry2.get(), self.addEntry3.get()))
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            A = app.d.showtable('team')
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            for record in A:
                self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2]))

    def edit_data(self):
        id = self.editEntryPrimkey.get()
        if id != '':
            attributes = []
            data = []
            name = self.editEntry2.get()
            if name != '':
                attributes.append('name')
                data.append(name)
            description = self.editEntry3.get()
            if description != '':
                attributes.append('description')
                data.append(description)
            table = 'team'
            primkey = 'teamid'
            app.d.change_entry(table, primkey, id, attributes, data)
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            A = app.d.showtable('team')
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            for record in A:
                self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2]))

    def delete_data(self):
        table = "team"
        primkey = "teamid"
        id = self.deleteEntry.get()
        app.d.delete_team(primkey,id)
        A = app.d.showtable('team')
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        for record in A:
            self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2]))

class ParticipantWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headLabel = tk.Label(self, text="VIEW & EDIT PARTICIPANTS", bg="grey")
        headLabel.configure(font=("Helvetica", 20, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=1, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        headLabel.grid_rowconfigure(0, weight=1)
        headLabel.grid_columnconfigure(0, weight=1)

        logout = tk.Button(self, text=" Log out  ", bg="grey",command=lambda: controller.show_frame(LoginPage))
        logout.grid(row=0, column=10, sticky="E")
        mainMenu = tk.Button(self, text=" Main Menu   ", bg="grey",command=lambda: controller.show_frame(MainMenu))
        mainMenu.grid(row=0, column=10, sticky="W")

        header = participationsHeader
        self.attrLabel1 = tk.Label(self, text=header[0])
        self.attrLabel1.grid(row=3, column=2)
        self.attrLabel2 = tk.Label(self, text=header[1])
        self.attrLabel2.grid(row=3, column=3)

        self.addLabel = tk.Label(self, text="Add")
        self.addLabel.grid(row=4, column=1, sticky="E")


        self.OPTIONS1 = controller.d.show1attribute('people', 'userid')
        self.w1_variable = tk.StringVar(self)
        self.w1_variable.set('UserID  ')  # default value
        self.w1 = tk.OptionMenu(self, self.w1_variable, *self.OPTIONS1)
        self.w1.grid(row=4, column=3, sticky='w')

        self.OPTIONS2 = controller.d.show1attribute('bookings', 'bookingid')
        self.w2_variable = tk.StringVar(self)
        self.w2_variable.set('BookingID  ')  # default value
        self.w2 = tk.OptionMenu(self, self.w2_variable, *self.OPTIONS2)
        self.w2.grid(row=4, column=2, sticky='w')

        self.addbutton = tk.Button(self, text="Add", command=self.insert_data)
        self.addbutton.grid(row=4, column=9)

        self.deleteLabel = tk.Label(self, text="Delete")
        self.deleteLabel.grid(row=6, column=1, sticky="E")

        self.OPTIONS3 = controller.d.show1attribute('people', 'userid')
        self.w3_variable = tk.StringVar(self)
        self.w3_variable.set('UserID  ')  # default value
        self.w3 = tk.OptionMenu(self, self.w3_variable, *self.OPTIONS3)
        self.w3.grid(row=6, column=3, sticky='w')

        self.OPTIONS4 = controller.d.show1attribute('bookings', 'bookingid')
        self.w4_variable = tk.StringVar(self)
        self.w4_variable.set('BookingID  ')  # default value
        self.w4 = tk.OptionMenu(self, self.w4_variable, *self.OPTIONS4)
        self.w4.grid(row=6, column=2, sticky='w')

        self.deletebutton = tk.Button(self, text="Delete", command=self.delete_data)
        self.deletebutton.grid(row=6, column=9)

        self.line2Label = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________",
                             bg="grey")
        self.line2Label.configure(font=("Helvetica", 20, "bold"))
        self.line2Label.grid(row=7, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        self.tree = tk.ttk.Treeview(self, columns=('1', '2'))
        self.tree.heading('#0', text=header[0])
        self.tree.heading('#1', text=header[1])
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.column('#1', stretch=Tkinter.YES)

        self.tree.grid(row=10, rowspan=20, columnspan=11, sticky='nsew')
        self.treeview = self.tree

        line3Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________",
                              bg="grey")
        line3Label.configure(font=("Helvetica", 20, "bold"))
        line3Label.grid(row=41, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        A = controller.d.showtable('participations')
        for user in A:
            self.treeview.insert('', 'end', text=user[0], values=(user[1]))

    def insert_data(self):
        attributes = participationsHeader
        data = [self.w1_variable.get(), self.w2_variable.get()]
        table = 'participations'
        try:
            app.d.insert_entry(table, attributes, data)
            print("Insert confirmed")
        except (psycopg2.IntegrityError):
            print("Already participating")
        self.treeview.insert('', 'end', text=self.w1_variable.get(), values=(
        self.w2_variable.get()))
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        A = app.d.showtable('participations')
        for record in A:
            self.treeview.insert('', 'end', text=record[0], values=(record[1]))

    def delete_data(self):
        table = "participations"
        primkey1 = 'bookingid'
        primkey2 = 'userid'
        id2 = self.w3_variable.get()
        id1 = self.w4_variable.get()
        app.d.delete_entry2(table, primkey1, primkey2, id1, id2)
        A = app.d.showtable('participations')
        while self.treeview.get_children():
            for t in self.treeview.get_children():
                self.treeview.delete(t)
        for record in A:
            self.treeview.insert('', 'end', text=record[0], values=(record[1]))
        print("Delete confirmed.")

class BookingsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.booking_variable = ''
        headLabel = tk.Label(self, text="VIEW & EDIT BOOKINGS", bg="grey")
        headLabel.configure(font=("Helvetica", 20, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=1, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        headLabel.grid_rowconfigure(0, weight=1)
        headLabel.grid_columnconfigure(0, weight=1)

        logout = tk.Button(self, text="  Log out      ", bg="grey",command=lambda: controller.show_frame(LoginPage))
        logout.grid(row=0, column=10, sticky="E")
        mainMenu = tk.Button(self, text="  Main Menu        ", bg="grey",command=lambda: controller.show_frame(MainMenu))
        mainMenu.grid(row=0, column=10, sticky="W")
        self.app=controller
        self.addLabel = tk.Label(self, text="Add")
        self.addLabel.grid(row=4, column=1, sticky="E")

        # --------------- ADD SELECTION DROP DOWN MENU START ---------------

        TIMES = ['00:00', '01:00', '02:00', '03:00', '04:00',
                 '05:00', '06:00', '07:00', '08:00', '09:00',
                 '10:00', '11:00', '12:00', '13:00', '14:00',
                 '15:00', '16:00', '17:00', '18:00', '19:00',
                 '20:00', '21:00', '22:00', '23:00']
        # date
        base2 = datetime.date.today()
        date_list = [base2 + datetime.timedelta(days=x) for x in range(0, 365)]
        self.date_variable = tk.StringVar(self)
        self.date_variable.set('Date     ')  # default value
        self.w2 = tk.OptionMenu(self, self.date_variable, *date_list)
        self.w2.grid(row=4, column=2, sticky='w')

        # start_time
        self.starttime_variable = tk.StringVar(self)
        self.starttime_variable.set('Start time     ')  # default value
        self.w3 = tk.OptionMenu(self, self.starttime_variable, *TIMES)
        self.w3.grid(row=4, column=2, sticky='e')

        # end_time
        self.endtime_variable = tk.StringVar(self)
        self.endtime_variable.set('End time     ')  # default value
        self.w4 = tk.OptionMenu(self, self.endtime_variable, *TIMES)
        self.w4.grid(row=4, column=3, sticky='w')

        # Room
        OPTIONS5 = controller.d.show1attribute('rooms','roomid')
        self.room_variable = tk.StringVar(self)
        self.room_variable.set('Room  ')  # default value
        self.w5 = tk.OptionMenu(self, self.room_variable, *OPTIONS5)
        self.w5.grid(row=4, column=3, sticky='e')

        # --------------- ADD SELECTION DROP DOWN MENU END ---------------

        self.addbutton = tk.Button(self, text="Add   ", command=self.insert_data)
        self.addbutton.grid(row=4, column=4, sticky='e')

        self.deleteLabel = tk.Label(self, text="Delete")
        self.deleteLabel.grid(row=6, column=1, sticky="E")

        # BOOKINGID-LIST
        self.OPTIONS1 = controller.d.show1attribute('bookings','bookingid')
        self.booking_variable = tk.StringVar(self)
        self.booking_variable.set('BookingID  ')  # default value
        self.w1 = tk.OptionMenu(self, self.booking_variable, *self.OPTIONS1)
        self.w1.grid(row=6, column=2, sticky='w')

        self.deletebutton = tk.Button(self, text="Delete", command=self.delete_data)
        self.deletebutton.grid(row=6, column=4, sticky='e')

        self.line2Label = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________",
                             bg="grey")
        self.line2Label.configure(font=("Helvetica", 20, "bold"))
        self.line2Label.grid(row=7, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        header=bookingsHeader
        self.tree = tk.ttk.Treeview(self, columns=('1', '2', '3', '4', '5'))
        self.tree.heading('#0', text=header[0])
        self.tree.heading('#1', text=header[2])
        self.tree.heading('#2', text=header[3])
        self.tree.heading('#3', text=header[4])
        self.tree.heading('#4', text=header[5])
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.column('#1', stretch=Tkinter.YES)
        self.tree.column('#2', stretch=Tkinter.YES)
        self.tree.column('#3', stretch=Tkinter.YES)
        self.tree.column('#4', stretch=Tkinter.YES)
        self.tree.grid(row=10, rowspan=20, columnspan=11, sticky='nsew')
        self.treeview = self.tree
        for column in ('1', '2', '3', '4', '5'):
            self.treeview.column(column, width=100)

        line3Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________",
                              bg="grey")
        line3Label.configure(font=("Helvetica", 20, "bold"))
        line3Label.grid(row=41, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        A = controller.d.showtable('bookings')
        for a in A:
            self.treeview.insert('', 'end', text=a[0], values=(a[1], a[2], a[3], a[4]))

    def insert_data(self):
        attributes = bookingsHeader2
        id = str(int(app.d.showLastID('bookings', 'bookingid'))+1)
        start = str(self.date_variable.get())+' '+str(self.starttime_variable.get())
        end = str(self.date_variable.get())+' '+str(self.endtime_variable.get())
        room = str(self.room_variable.get())
        user = str(app.loggedInUser)
        print(start)
        print(end)
        team = app.d.getTeamID(str(user))
        if app.d.key_is_ok('bookings', 'bookingid', id):
            data = [id, start, end, room, user, team]
            table = 'bookings'
            primkey = 'bookingid'
            app.d.insert_entry(table, attributes, data)

            for t in self.treeview.get_children():
                self.treeview.delete(t)
            A = self.app.d.showtable('bookings')
            for a in A:
                self.treeview.insert('', 'end', text=a[0], values=(a[1], a[2], a[3], a[4]))
            self.OPTIONS1 = self.app.d.show1attribute('bookings', 'bookingid')
            self.booking_variable = tk.StringVar(self)
            self.booking_variable.set('BookingID  ')  # default value
            self.w1 = tk.OptionMenu(self, self.booking_variable, *self.OPTIONS1)
            self.w1.grid(row=6, column=2, sticky='w')
            self.deletebutton = tk.Button(self, text="Delete", command=self.delete_data)
            self.deletebutton.grid(row=6, column=4, sticky='e')

    def delete_data(self):
        userid = str(app.loggedInUser)
        bookingid = str(self.booking_variable.get())
        app.d.delete_booking(userid, bookingid)
        A = self.app.d.showtable('bookings')
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        for a in A:
            self.treeview.insert('', 'end', text=a[0], values=(a[1], a[2], a[3], a[4]))
        self.OPTIONS1 = app.d.show1attribute('bookings', 'bookingid')
        self.booking_variable = tk.StringVar(self)
        self.booking_variable.set('BookingID  ')  # default value
        self.w1 = tk.OptionMenu(self, self.booking_variable, *self.OPTIONS1)
        self.w1.grid(row=6, column=2, sticky='w')
        self.deletebutton = tk.Button(self, text="Delete", command=self.delete_data)
        self.deletebutton.grid(row=6, column=4, sticky='e')

class RoomsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headLabel = tk.Label(self, text="VIEW & EDIT ROOMS", bg="grey")
        headLabel.configure(font=("Helvetica", 20, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=1, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        headLabel.grid_rowconfigure(0, weight=1)
        headLabel.grid_columnconfigure(0, weight=1)

        logout = tk.Button(self, text="  Log out      ", bg="grey",command=lambda: controller.show_frame(LoginPage))
        logout.grid(row=0, column=10, sticky="E")
        mainMenu = tk.Button(self, text="  Main Menu        ", bg="grey",command=lambda: controller.show_frame(MainMenu))
        mainMenu.grid(row=0, column=9, sticky="E")

        header = roomsHeader
        self.attrLabel1 = tk.Label(self, text=header[0])
        self.attrLabel1.grid(row=3, column=2)
        self.attrLabel2 = tk.Label(self, text=header[1])
        self.attrLabel2.grid(row=3, column=3)
        self.attrLabel3 = tk.Label(self, text=header[2])
        self.attrLabel3.grid(row=3, column=4)
        self.attrLabel4 = tk.Label(self, text=header[3])
        self.attrLabel4.grid(row=3, column=5)
        self.attrLabel5 = tk.Label(self, text=header[4])
        self.attrLabel5.grid(row=3, column=6)


        self.addLabel = tk.Label(self, text="Add")
        self.addLabel.grid(row=4, column=1, sticky="E")


        self.addEntry1 = tk.Entry(self)
        self.addEntry1.grid(row=4, column=2)
        self.addEntry2 = tk.Entry(self)
        self.addEntry2.grid(row=4, column=3)
        self.addEntry3 = tk.Entry(self)
        self.addEntry3.grid(row=4, column=4)
        self.addEntry4 = tk.Entry(self)
        self.addEntry4.grid(row=4, column=5)
        self.addEntry5 = tk.Entry(self)
        self.addEntry5.grid(row=4, column=6)

        self.addbutton = tk.Button(self, text="Add", command=self.insert_data)
        self.addbutton.grid(row=4, column=9)

        self.editLabel = tk.Label(self, text="Edit")
        self.editLabel.grid(row=5, column=1, sticky="E")
        self.editEntryPrimkey = tk.Entry(self)
        self.editEntryPrimkey.grid(row=5, column=2)
        self.editEntry2 = tk.Entry(self)
        self.editEntry2.grid(row=5, column=3)
        self.editEntry3 = tk.Entry(self)
        self.editEntry3.grid(row=5, column=4)
        self.editEntry4 = tk.Entry(self)
        self.editEntry4.grid(row=5, column=5)
        self.editEntry5 = tk.Entry(self)
        self.editEntry5.grid(row=5, column=6)

        self.editbutton = tk.Button(self, text="Edit", command=self.edit_data)
        self.editbutton.grid(row=5, column=9)

        self.deleteLabel = tk.Label(self, text="Delete")
        self.deleteLabel.grid(row=6, column=1, sticky="E")

        self.deleteEntry = tk.Entry(self)
        self.deleteEntry.grid(row=6, column=2)

        self.deletebutton = tk.Button(self, text="Delete", command=self.delete_data)
        self.deletebutton.grid(row=6, column=9)

        line2Label = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________",
                             bg="grey")
        line2Label.configure(font=("Helvetica", 20, "bold"))
        line2Label.grid(row=7, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        self.tree = tk.ttk.Treeview(self, columns=('1', '2', '3', '4'))
        self.tree.heading('#0', text=header[0])
        self.tree.heading('#1', text=header[1])
        self.tree.heading('#2', text=header[2])
        self.tree.heading('#3', text=header[3])
        self.tree.heading('#4', text=header[4])
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.column('#1', stretch=Tkinter.YES)
        self.tree.column('#2', stretch=Tkinter.YES)
        self.tree.column('#3', stretch=Tkinter.YES)
        self.tree.column('#4', stretch=Tkinter.YES)
        self.tree.grid(row=10, rowspan=20, columnspan=11, sticky='nsew')
        self.treeview = self.tree

        line3Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________",
                              bg="grey")
        line3Label.configure(font=("Helvetica", 20, "bold"))
        line3Label.grid(row=41, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        A = controller.d.showtable('rooms')
        for user in A:
            self.treeview.insert('', 'end', text=user[0], values=(user[1], user[2], user[3], user[4]))

    def insert_data(self):
        attributes = roomsHeader
        id = self.addEntry1.get()
        if app.d.key_is_ok('rooms', 'roomid', id):
            data = [id, self.addEntry2.get(), self.addEntry3.get(), self.addEntry4.get(),
                    self.addEntry5.get()]
            table = 'rooms'
            primkey = 'roomid'
            app.d.insert_entry(table, attributes, data)
            self.treeview.insert('', 'end', text=self.addEntry1.get(), values=(
            self.addEntry2.get(), self.addEntry3.get(), self.addEntry4.get(), self.addEntry5.get()))
            A = app.d.showtable('rooms')
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            for record in A:
                self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3], record[4]))

    def edit_data(self):
        id = self.editEntryPrimkey.get()
        if id != '':
            attributes = []
            data = []
            name = self.editEntry2.get()
            if name != '':
                attributes.append('name')
                data.append(name)
            price = self.editEntry3.get()
            if price != '':
                attributes.append('price')
                data.append(price)
            floor = self.editEntry4.get()
            if floor != '':
                attributes.append('floor')
                data.append(floor)
            capacity = self.editEntry5.get()
            if capacity != '':
                attributes.append('capacity')
                data.append(capacity)
            table = 'rooms'
            primkey = 'roomid'
            app.d.change_entry(table, primkey, id, attributes, data)
            while self.treeview.get_children():
                for t in self.treeview.get_children():
                    self.treeview.delete(t)
            A = app.d.showtable('rooms')
            for t in self.treeview.get_children():
                self.treeview.delete(t)
            for record in A:
                self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3], record[4]))

    def delete_data(self):
        table = "rooms"
        primkey = "roomid"
        id = self.deleteEntry.get()
        app.d.delete_entry(table, primkey, id)
        A = app.d.showtable('rooms')
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        for record in A:
            self.treeview.insert('', 'end', text=record[0], values=(record[1], record[2], record[3], record[4]))

class CostsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headLabel = tk.Label(self, text="VIEW & EDIT COSTS", bg="grey")
        headLabel.configure(font=("Helvetica", 20, "bold"))
        headLabel.grid(row=0, column=1, columnspan=10, rowspan=1, sticky="NWSE")
        self.app = controller
        lineLabel = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________", bg="grey")
        lineLabel.configure(font=("Helvetica", 20, "bold"))
        lineLabel.grid(row=1, column=1, columnspan=10, rowspan=1, sticky="NWSE")

        headLabel.grid_rowconfigure(0, weight=1)
        headLabel.grid_columnconfigure(0, weight=1)

        logout = tk.Button(self, text="  Log out      ", bg="grey",command=lambda: controller.show_frame(LoginPage))
        logout.grid(row=0, column=10, sticky="E")
        mainMenu = tk.Button(self, text="  Main Menu        ", bg="grey",command=lambda: controller.show_frame(MainMenu))
        mainMenu.grid(row=0, column=10, sticky="W")

        header = costsHeader
        self.attrLabel1 = tk.Label(self, text=header[0])
        self.attrLabel1.grid(row=3, column=2)
        self.attrLabel2 = tk.Label(self, text="From")
        self.attrLabel2.grid(row=3, column=3)
        self.attrLabel2 = tk.Label(self, text="To")
        self.attrLabel2.grid(row=3, column=4)

        hours = ['00:00:00', '01:00:00', '02:00:00', '03:00:00', '04:00:00',
                '05:00:00', '06:00:00', '07:00:00', '08:00:00', '09:00:00',
                '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00',
                '15:00:00', '16:00:00', '17:00:00', '18:00:00', '19:00:00',
                '20:00:00', '21:00:00', '22:00:00', '23:00:00', '24:00:00']

        base1 = datetime.date.today()
        date_list1 = [base1 - datetime.timedelta(days=x) for x in range(0, 365)]
        date_list2 = [base1 + datetime.timedelta(days=x) for x in range(1, 365)]
        date_list1.reverse()
        for elem in date_list2:
            date_list1.append(elem)

        # # Team
        # teamlist = controller.d.show1attribute('team', 'teamid')
        # self.team_variable = tk.StringVar(self)
        # self.team_variable.set('Team')  # default value
        # self.w5 = tk.OptionMenu(self, self.team_variable, *teamlist)
        # self.w5.grid(row=4, column=2)

        #From date
        self.date_variable1 = tk.StringVar(self)
        self.date_variable1.set(datetime.date.today())  # default value
        self.w1 = tk.OptionMenu(self, self.date_variable1, *date_list1)
        self.w1.grid(row=4, column=3, sticky='w')

        #From time
        self.starttime_variable = tk.StringVar(self)
        self.starttime_variable.set('00:00:00')  # default value
        self.w3 = tk.OptionMenu(self, self.starttime_variable, *hours)
        self.w3.grid(row=4, column=3, sticky='e')

        #To date
        self.date_variable2 = tk.StringVar(self)
        self.date_variable2.set(datetime.date.today())  # default value
        self.w2 = tk.OptionMenu(self, self.date_variable2, *date_list1)
        self.w2.grid(row=4, column=4, sticky='w')

        #To time
        self.endtime_variable = tk.StringVar(self)
        self.endtime_variable.set('00:00:00')  # default value
        self.w4 = tk.OptionMenu(self, self.endtime_variable, *hours)
        self.w4.grid(row=4, column=4, sticky='e')

        #Label & Button
        self.viewButton = tk.Button(self, text="View", command=self.show_data)
        self.viewButton.grid(row=4, column=9)

        self.line2Label = tk.Label(self, text="____________________________________________________________________________________________________________________________________________________",
                             bg="grey")
        self.line2Label.configure(font=("Helvetica", 20, "bold"))
        self.line2Label.grid(row=7, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        self.tree = tk.ttk.Treeview(self, columns=('1'))
        self.tree.heading('#0', text=header[0])
        self.tree.heading('#1', text=header[1])
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.column('#1', stretch=Tkinter.YES)

        self.tree.grid(row=10, rowspan=20, columnspan=11, sticky='nsew')
        self.treeview = self.tree

        line3Label = tk.Label(self,
                              text="____________________________________________________________________________________________________________________________________________________",
                              bg="grey")
        line3Label.configure(font=("Helvetica", 20, "bold"))
        line3Label.grid(row=41, column=1, columnspan=11, rowspan=1, sticky="NWSE")

        A = controller.d.groups_debit()
        for team in A:
            self.treeview.insert('', 'end', text=team[0], values=(team[1]))

    def show_data(self):
        start = str(self.date_variable1.get()) + ' ' + str(self.starttime_variable.get())
        end = str(self.date_variable2.get()) + ' ' + str(self.endtime_variable.get())
        print(start)
        print(end)
        A=self.app.d.costs_for_period(start, end)
        for t in self.treeview.get_children():
            self.treeview.delete(t)
        for a in A:
            self.treeview.insert('', 'end', text=a[0], values=(a[1]))


# Main ------------------------------
app = MeetifyApp()
app.mainloop()