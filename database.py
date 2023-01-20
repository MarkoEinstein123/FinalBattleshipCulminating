from tabulate import tabulate
import os
import sqlite3
import sys
import tty
import termios

#database variables
global database
database_highscore = []
database_file = "database.txt"

#writes to the database.txt file using updated database.txt file
def write_file():
    with open(database_file, "w") as txt_file:
        for line in database:
            txt_file.write(",".join(line) + "\n")

#reads the database.txt file and returns the values as database
def read_file():
    try:
        with open(database_file, 'r') as read_file:
            database = [line.strip().split(',') for line in read_file]
        return database      
    except IOError:
        print("File not accessible")
    except FileNotFoundError:
        print("File does not exist")


def write_table(shots_left):
    highscore = 60 - shots_left 
    database.pop(0)
    new_row = [str(highscore)]
    database.append(new_row)
    write_file()

database = read_file()