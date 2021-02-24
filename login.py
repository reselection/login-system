#!/bin/python3
import sqlite3
import base64
import time

def start_menu():
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

def login(username, password):
    """
    Talks to the database to log the user in if credentials are correct.
    """
    pass

def data_storage(data):
    """
    After logging in this function will store desired data for user.
    """
    pass

start_menu()
