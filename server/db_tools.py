import sqlite3

from datetime import datetime

import pathlib

HOME = pathlib.Path(__file__).parent.absolute()

db = sqlite3.connect(HOME/'test.db')

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
    db.execute(
f"""
INSERT INTO {name} (timestamp, website, category, co2_emissions, logo_url)
VALUES ("{timestamp}", "{website}", "{category}", {co2_emissions}, "{logo_url}");
"""
)

    db.commit()
    
def get_websites(name):
    categories = list( # SELECT DISTINCT ...
        {x[0] for x in db.execute(f"SELECT category FROM {name}").fetchall()}
    )
    print(categories)
    for category in categories:
        rows = db.execute(f"SELECT category, website, logo_URL, co2_emissions FROM {name} WHERE category = '{category}'").fetchall()
        print(rows)

    #return db.execute(f"SELECT website, logo_URL, category, co2_emissions FROM {name} ORDER BY timestamp").fetchall()

def data_over_time(name):
    data = db.execute(f"SELECT timestamp, co2_emissions FROM {name} ORDER BY timestamp").fetchall()
    return sorted(data)

def data_points(name):
    points = db.execute(f"SELECT timestamp, co2_emissions FROM {name} ORDER BY timestamp").fetchall()
    # Starting from the second value, add the previous total to the current value to calculate the overall total at a given time
    for i, (time, value) in enumerate(points[1:]):
        points[i+1] = (time, value + points[i][1])
    return points

if __name__ == '__main__':
    update_row('Ryan', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'www.example.com', 'Transportation', 50, 'www.example.com/logo.png')
    update_row('Ryan', '2023-02-05 12:00:00', 'www.example.com', 'Food', 30, 'www.example.com/logo.png')
    update_row('Ryan', '2023-02-06 12:00:00', 'www.anothersite.com', 'Electricity', 40, 'www.anothersite.com/logo.png')
    update_row('Ryan', '2023-02-07 12:00:00', 'www.yetanotherexample.com', 'Transportation', 60, 'www.yetanotherexample.com/logo.png')
    update_row('Ryan', '2023-02-08 12:00:00', 'www.example.com', 'Food', 25, 'www.example.com/logo.png')
    update_row('Jim', '2023-02-09 12:00:00', 'www.anothersite.com', 'Electricity', 35, 'www.anothersite.com/logo.png')
    update_row('Jim', '2023-02-06 12:00:00', 'www.anothersite.com', 'Electricity', 40, 'www.anothersite.com/logo.png')
    update_row('Alex', '2023-02-07 12:00:00', 'www.yetanotherexample.com', 'Transportation', 60, 'www.yetanotherexample.com/logo.png')
    update_row('Alex', '2023-02-08 12:00:00', 'www.example.com', 'Food', 25, 'www.example.com/logo.png')
    update_row('Jack', '2023-02-09 12:00:00', 'www.anothersite.com', 'Electricity', 35, 'www.anothersite.com/logo.png')
    print(data_points('Ryan'))
