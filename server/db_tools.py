import sqlite3
import pathlib
import json
import random
import string
import hashlib
from datetime import datetime

HOME = pathlib.Path(__file__).parent.absolute()

db = sqlite3.connect(HOME/'test.db',check_same_thread=False)

def update_row(name, timestamp, website, category, co2_emissions, logo_url):
    db.execute(
f"""
CREATE TABLE IF NOT EXISTS {name} (
  timestamp TIMESTAMP NOT NULL,
  website VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  co2_emissions FLOAT NOT NULL,
  logo_url VARCHAR(255) NOT NULL,
  PRIMARY KEY (timestamp)
);
"""
)
    day = timestamp.split()[0]
    exists = db.execute(f"SELECT timestamp, co2_emissions FROM '{name}' WHERE website = '{website}'").fetchall()
    exists = list(filter(lambda x: x[0].split()[0] == day, exists))
    if len(exists) > 0:
        newTotal = exists[0][1] + co2_emissions
        db.execute(
            f"""
            UPDATE '{name}' SET co2_emissions='{newTotal}' WHERE timestamp='{exists[0][0]}'
            """
        )
        db.commit()
    else:
        db.execute(
    f"""
    INSERT INTO {name} (timestamp, website, category, co2_emissions, logo_url)
    VALUES ("{timestamp}", "{website}", "{category}", {co2_emissions}, "{logo_url}");
    """
    )

        db.commit()
    
def getCategories(name):
    categories = list( # SELECT DISTINCT ...
        {x[0] for x in db.execute(f"SELECT category FROM {name}").fetchall()}
    )
    print(categories)
    categoryDict = {}
    for category in categories:
        entries = []
        rows = db.execute(f"SELECT category, website, logo_URL, co2_emissions FROM {name} WHERE category = '{category}'").fetchall()
        for entry in rows:
            values = {
                "name": entry[1],
                "icon": entry[2],
                "amount": entry[3],
            }
            entries.append(values)
        categoryDict[category] = entries
    categoryDict = {k:{"sites":v} for k,v in categoryDict.items()}
    return json.dumps(categoryDict)

    #return db.execute(f"SELECT website, logo_URL, category, co2_emissions FROM {name} ORDER BY timestamp").fetchall()

def loadGraph(name):
    points = db.execute(f"SELECT timestamp, co2_emissions FROM {name} ORDER BY timestamp").fetchall()
    # Starting from the second value, add the previous total to the current value to calculate the overall total at a given time
    for i, (time, value) in enumerate(points[1:]):
        points[i+1] = (time, value + points[i][1])
    return json.dumps(points)

def lastMonthData(name):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lastMonth = '0' + str(int(timestamp.split()[0].split('-')[1]) - 1)
    categories = [x[0] for x in db.execute(f"SELECT DISTINCT category FROM '{name}'").fetchall()]
    categoryTotals = {}
    for category in categories:
        emissions = db.execute(f"SELECT timestamp, co2_emissions FROM '{name}' WHERE category='{category}'").fetchall()
        emissions = list(filter(lambda x: x[0].split()[0].split('-')[1] == lastMonth, emissions))
        categoryTotals[category] = sum(map(lambda x: x[1], emissions))
    return json.dumps(categoryTotals)
    


    print(categories)

def register(name, password):
    letters = string.ascii_lowercase
    salt = ''.join(random.choice(letters) for i in range(20))
    dbPassword = password+salt
    hash = hashlib.sha256(dbPassword.encode()).hexdigest()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    # Insert the new user into the users table
    db.execute("""
        INSERT INTO users (name, hash, salt)
        VALUES (?, ?, ?)
    """, (name, hash, salt))

    # Commit the changes and close the database connection
    db.commit()


# Run on login
def validate(name, password):
    salt = db.execute("SELECT salt FROM users WHERE name=?", (name,)).fetchall()
    if len(salt) == 0:
        return False
    hash = hashlib.sha256((password + salt[0][0]).encode()).hexdigest()
    result = db.execute("SELECT name, hash FROM users WHERE name=? AND hash=?", (name, hash)).fetchall()
    if len(result) > 0:
        return True
    else:
        return False
    
def login(name, password):
    if validate(name, password):
        return [getCategories(name), loadGraph(name)]
    else:
        return False

def addRelation(name1, name2, type):
    assert type in ["friends", "local"]
    db.execute(f"""
        CREATE TABLE IF NOT EXISTS '{type}' (
            name1 TEXT NOT NULL,
            name2 TEXT NOT NULL
        )
    """)

    try:

        db.execute(f"""INSERT INTO '{type}' (name1, name2)
        VALUES (?, ?)
        """, (name1, name2))

        db.commit()

        return loadGraph(name2).split()[-1][:-2]
    
    except:

        return False

def leaderboard(name, type):
    assert type in ["friends", "local"]
    friendsList = db.execute(f"SELECT name2 FROM '{type}' WHERE name1='{name}'").fetchall()
    if len(friendsList) == 0:
        return False
    else:
        friendsList = [(friendName[0], loadGraph(friendName[0]).split()[-1][:-2]) for friendName in friendsList]
        friendsList.sort(key=lambda x: float(x[1]))
        return json.dumps(friendsList)

if __name__ == '__main__':
    update_row('Ryan', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'www.example.com', 'Transportation', 50, 'www.example.com/logo.png')
    update_row('Ryan', '2023-02-05 12:00:00', 'www.example.com', 'Food', 30, 'www.example.com/logo.png')
    update_row('Ryan', '2023-02-05 12:05:00', 'www.example.com', 'Food', 30, 'www.example.com/logo.png')
    update_row('Ryan', '2023-02-06 12:00:00', 'www.anothersite.com', 'Electricity', 40, 'www.anothersite.com/logo.png')
    update_row('Ryan', '2023-02-06 12:10:00', 'www.anothersite.com', 'Electricity', 40, 'www.anothersite.com/logo.png')
    update_row('Ryan', '2023-02-07 12:00:00', 'www.yetanotherexample.com', 'Transportation', 60, 'www.yetanotherexample.com/logo.png')
    update_row('Ryan', '2023-02-08 12:00:00', 'www.example.com', 'Food', 25, 'www.example.com/logo.png')
    update_row('Ryan', '2023-01-15 12:05:00', 'www.example.com', 'Food', 70, 'www.example.com/logo.png')
    update_row('Ryan', '2023-01-05 12:05:00', 'www.example.com', 'Food', 10, 'www.example.com/logo.png')
    update_row('Ryan', '2023-01-16 12:00:00', 'www.anothersite.com', 'Electricity', 20, 'www.anothersite.com/logo.png')
    update_row('Jim', '2023-02-09 12:00:00', 'www.anothersite.com', 'Electricity', 35, 'www.anothersite.com/logo.png')
    update_row('Jim', '2023-02-06 12:00:00', 'www.anothersite.com', 'Electricity', 40, 'www.anothersite.com/logo.png')
    update_row('Alex', '2023-02-07 12:00:00', 'www.yetanotherexample.com', 'Transportation', 60, 'www.yetanotherexample.com/logo.png')
    update_row('Alex', '2023-02-08 12:00:00', 'www.example.com', 'Food', 25, 'www.example.com/logo.png')
    update_row('Jack', '2023-02-09 12:00:00', 'www.anothersite.com', 'Electricity', 35, 'www.anothersite.com/logo.png')
    register("Jim", "abc")
    register("Ryan", "abc")
    register("Jack", "abc")
    register("Alex", "abc")
    print(addRelation("Ryan", "Jim", "friends"))
    print(addRelation("Ryan", "Alex", "friends"))
    print(addRelation("Ryan", "Jack", "friends"))
    print(leaderboard("Ryan", "friends"))
    print(addRelation("Jim", "Alex", "local"))
    print(addRelation("Jim", "Jack", "local"))
    print(addRelation("Jim", "Ryan", "local"))
    print(leaderboard("Jim", "local"))
    print(lastMonthData("Ryan"))
    