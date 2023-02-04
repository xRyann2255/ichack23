import sqlite3

import pathlib

HOME = pathlib.Path(__file__).parent.absolute()

db = sqlite3.connect(HOME/'test.db')

def update_row(name, timestamp, website, category, co2_emissions, logo_url):
    c = db.cursor()
    c.execute(
    



