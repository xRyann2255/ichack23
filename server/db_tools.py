import sqlite3

import pathlib

HOME = pathlib.Path(__file__).parent.absolute()

db = sqlite3.connect(HOME/'test.db')

def update_row(name, timestamp, website, category, co2_emissions, logo_url):
    db.execute(
f"""
CREATE TABLE IF NOT EXISTS main.{name} (
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
INSERT INTO main.{name} (timestamp, website, category, co2_emissions, logo_url)
VALUES ('{timestamp}', '{website}', '{category}', '{co2_emissions}', '{logo_url}');
"""
)

update_row('Ryan', '2023-02-04 12:00:00', 'www.example.com', 'Transportation', 50, 'www.example.com/logo.png')
update_row('Ryan', '2023-02-05 12:00:00', 'www.example.com', 'Food', 30, 'www.example.com/logo.png')
update_row('Ryan', '2023-02-06 12:00:00', 'www.anothersite.com', 'Electricity', 40, 'www.anothersite.com/logo.png')
update_row('Ryan', '2023-02-07 12:00:00', 'www.yetanotherexample.com', 'Transportation', 60, 'www.yetanotherexample.com/logo.png')
update_row('Ryan', '2023-02-08 12:00:00', 'www.example.com', 'Food', 25, 'www.example.com/logo.png')
update_row('Jim', '2023-02-09 12:00:00', 'www.anothersite.com', 'Electricity', 35, 'www.anothersite.com/logo.png')
update_row('Jim', '2023-02-06 12:00:00', 'www.anothersite.com', 'Electricity', 40, 'www.anothersite.com/logo.png')
update_row('Alex', '2023-02-07 12:00:00', 'www.yetanotherexample.com', 'Transportation', 60, 'www.yetanotherexample.com/logo.png')
update_row('Alex', '2023-02-08 12:00:00', 'www.example.com', 'Food', 25, 'www.example.com/logo.png')
update_row('Jack', '2023-02-09 12:00:00', 'www.anothersite.com', 'Electricity', 35, 'www.anothersite.com/logo.png')




