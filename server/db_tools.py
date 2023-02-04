import sqlite3

db = sqlite3.connect('test.db')

c = db.cursor()
c.execute(
"""
CREATE DATABASE carbon_footprint;

-- Use the database
USE carbon_footprint;

-- Create a template for user tables
CREATE TABLE user_template (
  timestamp TIMESTAMP NOT NULL,
  website VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  co2_emissions FLOAT NOT NULL,
  logo_url VARCHAR(255) NOT NULL
);
"""
)