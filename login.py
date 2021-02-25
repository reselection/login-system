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
        time.sleep(3)
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
            time.sleep(3)
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
        if username not in match:
            print("Account not found\nReturning...")
            time.sleep(1)
            login()
        elif data[0] == username and x.decode() == password:
            print("You've logged in\nRedirecting...")
            time.sleep(3)
            user_panel(username)
        else:
            continue


def data_storage(data):
    """
    After logging in this function will store desired data for user.
    """
    pass

def user_panel(username):
    x = username
    
    print(f"Welcome {username}")
    print("Type info to see all commands")
    
    request = input(f"{username}: ")
    if request == 'info':
        print("(1)Store info.\n(2)Retrieve data.\n(3)Change password.\n(4)Log out.\n(5)Close program")
        user_panel(x)
    elif request == '1':
        print("1")
    elif request == '2':
        print("2")
    elif request == '3':
        print("3")
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
        user_panel(x)


def admin_panel():
    '''Panel for admin'''
    print("Type 'info' for help")
    request = input(": ")
    admin_panel()

start_menu()
