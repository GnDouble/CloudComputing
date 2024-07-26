import sqlite3

con = sqlite3.connect('plant.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS plants
        (plant_id INT, plant_name TEXT)''')