import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Management")

connection = sqlite3.connect('management.db')

TABLE_NAME = "management_table"
STUDENT_ID = "student_id"
STUDENT_FNAME = "student_firstname"
STUDENT_LNAME = "student_lastname"
STUDENT_TNUMBER = "student_address"

connection.execute(" CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ( " + STUDENT_ID +
                   " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                   STUDENT_FNAME + " TEXT, " + STUDENT_LNAME + " TEXT, " +
                   STUDENT_TNUMBER + " TEXT);")

appLabel = tk.Label(root, text="Student Management System", fg="#06a099", width=35)
appLabel.config(font=("Sylfaen", 30))
appLabel.grid(row=0, columnspan=2, padx=(10, 10), pady=(30, 0))


class Student:
    student_firstname = ""
    student_lastname = ""
    number = ""

    def __init__(self, student_firstname, student_lastname, number):
        self.student_firstname = student_firstname
        self.student_lastname = student_lastname
        self.number = number


nameLabel = tk.Label(root, text="Student first name", width=40, anchor='w',
                     font=("Sylfaen", 12)).grid(row=1, column=0, padx=(10, 0),
                                                pady=(30, 0))
collegeLabel = tk.Label(root, text="Student last name", width=40, anchor='w',
                        font=("Sylfaen", 12)).grid(row=2, column=0, padx=(10, 0))

addressLabel = tk.Label(root, text="Student T-number", width=40, anchor='w',
                        font=("Sylfaen", 12)).grid(row=4, column=0, padx=(10, 0))

fNameEntry = tk.Entry(root, width=30)
lNameEntry = tk.Entry(root, width=30)
studentNum = tk.Entry(root, width=30)

fNameEntry.grid(row=1, column=1, padx=(0, 10), pady=(30, 20))
lNameEntry.grid(row=2, column=1, padx=(0, 10), pady=20)
studentNum.grid(row=4, column=1, padx=(0, 10), pady=20)


def takeNameInput():
    global fNameEntry, lNameEntry, studentNum
    global list
    global TABLE_NAME, STUDENT_FNAME, STUDENT_LNAME, STUDENT_TNUMBER  # Remove STUDENT_PHONE
    fname = fNameEntry.get()
    fNameEntry.delete(0, tk.END)
    lname = lNameEntry.get()
    lNameEntry.delete(0, tk.END)
    t_num = studentNum.get()
    studentNum.delete(0, tk.END)

    connection.execute("INSERT INTO " + TABLE_NAME + " ( " + STUDENT_FNAME + ", " +
                       STUDENT_LNAME + ", " + STUDENT_TNUMBER + " ) VALUES ( '"
                       + fname + "', '" + lname + "', '" +
                       t_num + "'); ")
    connection.commit()
    messagebox.showinfo("Success", "Data Saved Successfully.")

def deleteTableIfExists():
    try:
        connection.execute("DROP TABLE IF EXISTS " + TABLE_NAME + ";")
        connection.commit()
        messagebox.showinfo("Success", "Table Deleted Successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def destroyRootWindow():
    root.destroy()
    secondWindow = tk.Tk()

    secondWindow.title("Display results")

    appLabel = tk.Label(secondWindow, text="Student Management System",
                        fg="#06a099", width=40)
    appLabel.config(font=("Sylfaen", 30))
    appLabel.pack()

    tree = ttk.Treeview(secondWindow)
    tree["columns"] = ("one", "two", "three", "four")

    tree.heading("one", text="Student Name")
    tree.heading("two", text="College Name")
    tree.heading("three", text="Address")
    tree.heading("four", text="img")

    cursor = connection.execute("SELECT * FROM " + TABLE_NAME + " ;")
    i = 0

    for row in cursor:
        tree.insert('', i, text="Student " + str(row[0]),
                    values=(row[1], row[2],
                            row[3], row[4]))
        i = i + 1

    tree.pack()
    secondWindow.mainloop()


# def printDetails():
#     for singleItem in list:
#         print("Student name is: %s\nCollege name is: %s\nPhone number is: %d\nAddress is: %s" %
#               (singleItem.studentName, singleItem.collegeName, singleItem.phoneNumber, singleItem.address))
#         print("****************************************")

button = tk.Button(root, text="Take input", command=lambda: takeNameInput())
button.grid(row=5, column=0, pady=30)

displayButton = tk.Button(root, text="Display result", command=lambda: destroyRootWindow())
displayButton.grid(row=5, column=1)

root.mainloop()
