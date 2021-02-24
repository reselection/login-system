#!/bin/python3
import sqlite3
import base64
import time

def start_menu():
    print("Welcome to log-database")
    print("(1) Login")
    print("(2) Create account")
    start = input(": ")
    if start == '1':
        login()
    elif start == '2':
        create_account()
    else:
        print(f"{start} is not a valid option, please try again")
        time.sleep(3)
        start_menu()

def create_account():
    """
    This function will create an account if the user hasn't yet, or wants another.
    """
    pass

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
