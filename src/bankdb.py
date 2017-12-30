#procedures to save and retrieve persistent database of problems using pickle
import pickle
import sys
import os
from loadbank import loadstandards, loadbank

def savebank(bank):
    """Saves persistent record of problem bank using pickle

    bank - dictionary of standard:list of problems
    saves bank.pickle in ~/GitHub/mathai/db"""

    dbdir = "/Users/chris/GitHub/mathai/db/"
    bankfile = dbdir + 'bank.pickle'
    with open(bankfile, 'wb') as f:
        # Pickle the 'bank' dictionary using the highest protocol available.
        pickle.dump(bank, f, pickle.HIGHEST_PROTOCOL)

def loaddb(dbfile):
    """Retrieves persistent record of problems using Pickle

    dbfile - name of file to load, from ~/GitHub/mathai/db, ending '.pickle'"""
    dbdir = "/Users/chris/GitHub/mathai/db/"
    filename = dbdir + dbfile + '.pickle'
    with open(filename, 'rb') as f:
        return pickle.load(f)
