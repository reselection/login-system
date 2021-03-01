#!/bin/python3
import sqlite3
import base64
import time
import subprocess
import os

def start_menu():
    if os.name == 'posix':
        subprocess.Popen('clear')
        time.sleep(1)
    elif os.name == 'nt':
        subprocess.Popen('test&cls')
        time.sleep(1)
    print("Welcome to log-database")
    print("(1) Login")
    print("(2) Create account")
    print("(3) Close application")
    start = input(": ")
    if start == '1':
        login()
    elif start == '2':
        create_account()
    elif start == '3':
        quit()
    else:
        print(f"{start} is not a valid option, please try again")
        time.sleep(1)
        start_menu()

def create_account():
    """
    This function will create an account if the user hasn't yet, or wants another.
    """
    conndb = sqlite3.connect('data/login-system.db')
    cursor = conndb.cursor()
    try:
        cursor.execute("CREATE TABLE user_data(user,password)")
    except:
        print("Table found")
        pass
    print("Type 'quit' to exit")
    username = input("Enter username: ")
    if username == 'quit':
        quit()
    password = input("Enter password: ")
    if password == 'quit':
        quit()
    
    cursor.execute("SELECT * FROM user_data")
    match = cursor.fetchall()
    
    for data in match:
        if data[0] == username:
            print("Username is taken\nTry again.")
            time.sleep(1)
            create_account()
     
    
    cursor.execute("INSERT INTO user_data(user,password) VALUES (?,?)", (username, base64.b64encode(password.encode('utf-8'))))

    conndb.commit()
    conndb.close()
    print("Account created to local database.\nReturning to menu...")
    time.sleep(3)
    start_menu()

def login():
    """
    Talks to the database to log the user in if credentials are correct.
    """
    conndb = sqlite3.connect('data/login-system.db')
    cursor = conndb.cursor()

    print("Enter 'return' to go to main menu.\nEnter quit to exit.")

    username = input("Enter username: ")
    if username == 'quit':
        quit()
    elif username == 'return':
        startmenu()
    password = input("Enter password: ")
    if password == 'quit':
        quit()
    elif password == 'return':
        start_menu()

    cursor.execute("SELECT * FROM user_data")
    match = cursor.fetchall() 
    
    for data in match:
        x = base64.b64decode(data[1])
        if username not in data:
            continue
        elif data[0] == 'admin' and x.decode() == password:
            print("Welcome, Admin.")
            time.sleep(2)
            admin_panel()
        elif data[0] == username and x.decode() == password:
            print("You've logged in\nRedirecting...")
            time.sleep(3)
            user_panel(username)
        else:
            print("Account not found")
            time.sleep(1)
            login()
        print("Account not found")
        time.sleep(1)
        login()


def data_storage(data):
    """
    After logging in this function will store desired data for user.
    """
    pass

def user_panel(username):
    """
    User can view options here and issue commands to change password, store info or retrieve it, and logout/close the program
    """
    conndb = sqlite3.connect('data/login-system.db')
    cursor = conndb.cursor()

    print(f"Welcome {username}")
    print("Type info to see all commands")
    
    request = input(f"{username}: ")
    if request == 'info':
        print("(1)Store info.\n(2)Retrieve data.\n(3)Change password.\n(4)Log out.\n(5)Close program")
        user_panel(username)
    elif request == '1':
        print("1")
        user_panel(username)
    elif request == '2':
        print("2")
    elif request == '3':
        cursor.execute("SELECT * FROM user_data")
        match = cursor.fetchall()
        old_password = input("Enter old password: ")
        for data in match:
            x = base64.b64decode(data[1])
            if username not in data:
                continue
            elif data[0] == username and x.decode() == old_password:
                new_password =          input("Enter new password: ")
                confirm_new_password =  input("Enter new password: ")
                if new_password == confirm_new_password:
                    new_encryption_password = base64.b64encode(new_password.encode('utf-8'))
                    print(f"user:{username} password:{new_encryption_password}")
                    time.sleep(1)
                    cursor.execute("UPDATE user_data SET password = (?) WHERE user = (?) AND password = (?)", (new_encryption_password, username,  base64.b64encode(old_password.encode('utf-8'))))
                    conndb.commit()
                    conndb.close()
                    print("Password changed")
                    time.sleep(1)
                    user_panel(username)
            print("Wrong password, try again.")
            user_panel(username)
    elif request == '4':
        print("Logging out...")
        time.sleep(1)
        start_menu()
    elif request == '5':
        print("Closing now...")
        time.sleep(1)
        quit()
    else:
        print("Not a valid command")
        time.sleep(1)
        user_panel(username)

def admin_panel():
    '''Panel for admin'''
    print("Type 'info' for help")
    request = input(": ")
    if request == 'info':
        print('(1):Change password')
    admin_panel()

start_menu()
