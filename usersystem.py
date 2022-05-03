import pandas as pd
import os
import time
import sqlite3

#Standart Username and Password --> root, root
con = sqlite3.connect("database.db")

cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, surname TEXT, id TEXT, email TEXT, grade TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS admin (username TEXT, password TEXT, name TEXT)")

def cls():
    """
    Clear Console Screen
    if NT --> use 'cls'
    if Linux/Mac --> use 'clear'
    """
    os.system('cls' if os.name=='nt' else 'clear') # clear function


class Students:
    """
    Register Student System 
    Give --> Name, Surname, ID, Email, Grade 
    Add datas to SQLite Database
    """
    counter = 0
    def __init__(self, name, surname, id, email, grade):
        self.name = name
        self.surname = surname
        self.id = id
        self.mail = email
        self.grade = grade

        Students.counter += 1
        ids = cursor.execute("SELECT id FROM users")
        for i in ids:
            if self.id in i:
                print("ID already exists")
                Students.counter -= 1
                self.id = input("Enter new ID: ")
            else:
                break
        mails = cursor.execute("SELECT email FROM users")
        for i in mails:
            if self.mail in i:
                print("Email already exists")
                Students.counter -= 1
                self.mail = input("Enter new Email: ")
            else:
                break
        
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (self.name, self.surname, self.id, self.mail, self.grade))
        con.commit()

    def users():
        dataFrameTest = pd.read_sql_query("SELECT * FROM users", con)
        print(dataFrameTest)

        print("\n" * 2)
#- Test Start -#
#Students("Tylor", "Durden", "Mezun", "tylor@durden.com", "Mezun") # :D Tylor Durden
#Students("Furkan", "Şimşek", "477", "furkansimsek@duck.com","7") # It's Me... yes I'm Student 
#Students.users()
#- This Codes Are Tested and Working. -#

def addUser():
    """
    Add User to SQLite Database (Students Class)
    """
    name = input("Name: ")
    surname = input("Surname: ")
    id = input("ID: ")
    email = input("Email: ")
    grade = input("Grade: ")
    
    Students(name, surname, id, email, grade)

def deleteStudent(): # Error --> Copy Student 22.02 --> 25.04.2022 --> Fixed
    #Delete Students With SQL
    """
    Delete user from SQLite Database
    """
    id = input("ID: ")
    cursor.execute("DELETE FROM users WHERE id = ?", id)
    con.commit()

def updateStudent():
    """
    Update Student Information
    """
    #Update users with SQL
    id = input("ID: ")
    name = input("Name: ")
    surname = input("Surname: ")
    email = input("Email: ")
    grade = input("Grade: ")
    cursor.execute("UPDATE users SET name = ?, surname = ?, email = ?, grade = ? WHERE id = ?", (name, surname, email, grade, id))

def searchStudent():
    """
    5 type to Seach User 
    1 -> Name
    2 -> Surname
    3 -> ID
    4 -> Email
    5 -> Grade
    """
    cls()
    print("Name search --> 1;\nSurname search --> 2;\nID search --> 3;\nEmail search --> 4;\n Grade search --> 5")
    question = input("Search Type: ")
    if question == "1":
        name = input("Name: ")    
        dataFrame = pd.read_sql_query("SELECT * FROM users WHERE name = ?", con, params=(name))
    elif question == "2":
        surname = input("Surname: ")
        dataFrame = pd.read_sql_query("SELECT * FROM users WHERE surname = ?", con, params=(surname))
    elif question == "3":
        id = input("ID: ")
        dataFrame = pd.read_sql_query("SELECT * FROM users WHERE id = ?", con, params=(id))
    elif question == "4":
        email = input("Email: ")
        dataFrame = pd.read_sql_query("SELECT * FROM users WHERE email = ?", con, params=(email))
    elif question == "5":
        grade = input("Grade: ")
        dataFrame = pd.read_sql_query("SELECT * FROM users WHERE grade = ?", con, params=(grade))
    print(dataFrame)        

def addAdmin():
    """
    Add Admin User
    """
    cls()
    username = input("Username: ")
    password = input("Password: ")
    while True:
        cursor.execute("SELECT username FROM admin WHERE = ?", username)
        if cursor.fetchone() :
            print("Username already exists!")
            username = input("Username: ")
        else:
            break
    name = input("Name: ")
    cursor.execute("INSERT INTO admin VALUES (?, ?, ?)", (username, password, name))
    con.commit()
def delAdmin():
    """
    Delete Admin User
    """
    username = input("Username: ")
    cursor.execute("DELETE FROM admin WHERE username = ?", username)
    con.commit()
    
def listAdmin():  
    """
    List Admin Users
    """  
    print(pd.read_sql_query("SELECT * FROM admin", con))
    
def welcomeScreen(name):
    """
    Operations Screens
    """
    while True:
        print("\n" * 3)
        print("Welcome to Student Management System,", name, "!")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Update Student")
        print("4. Search Student")
        print("5. List Student")
        print("6. Add Admin User")
        print("7. Delete Admin User")
        print("8. List Admin User")
        print("9. Exit")

        question = input("What do you want to do? \n > ")
        cls()
        if question == "1":
            cls()
            addUser()
        elif question == "2":
            cls()
            deleteStudent()
        elif question == "3":
            cls()
            updateStudent()
        elif question == "4":
            cls()
            searchStudent()
        elif question == "5":
            cls()
            Students.users()
        elif question == "6":
            cls()
            addAdmin()
        elif question == "9":
            cls()
            print("Good Bye!")
            time.sleep(1)
            break
        elif question == "7":
            cls()
            delAdmin()
        elif question == "8":
            cls()
            listAdmin()
        else:
            cls()
            print("Wrong Input!")

def login():
    """
    Login
    """
    cls()
    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
    if cursor.fetchone() :
        cursor.execute("SELECT name FROM admin WHERE username = ? AND password = ?", (username, password))
        cls()
        welcomeScreen(cursor.fetchone()[0])

    print(cursor.fetchone())
   
def main():
    """
    Main Function
    """
    cls()
    print("1. Login")
    print("2. Exit")
    question = input("What do you want to do? \n > ")

    if question == "1":
        login()
        main()
    elif question == "2":
        print("Good Bye!")
    else:
        print("Wrong Input!")
        main()

main()