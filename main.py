import os
import datetime
import sqlite3
from discordwebhook import Discord
from flask import Flask, render_template, request
from datetime import datetime,timedelta
from dotenv import load_dotenv, dotenv_values

app = Flask(__name__)

def open_and_connect_db():
    con = sqlite3.connect("mydatabase", check_same_thread=False)
    cursor = con.cursor()

# SQLite database setup
con = sqlite3.connect("mydatabase", check_same_thread=False)
cursor = con.cursor()

# Create the 'messages' table if it doesn't exist
cursor.execute('CREATE TABLE IF NOT EXISTS mydatabase (id INTEGER PRIMARY KEY, time_of_input TIMESTAMP, text TEXT)')

# Function that get data and insert to 'mydatabase' table
def insert_to_table(data):
    open_and_connect_db()
    x = str(data)
    cursor.execute("INSERT INTO mydatabase (time_of_input, text) VALUES (?, CURRENT_TIMESTAMP)", (x,))
    con.commit()
    return "Must to return value"

#Function that get data and sent it to Discord Bot
def send_to_discord(data):
    open_and_connect_db()
    x = str(data)
    load_dotenv()
    url = os.getenv("url")
    discord = Discord(url=url)
    discord.post(content=x)
    return "Must to return value"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data", methods=["POST"])
def get_input():
    open_and_connect_db()
    data = request.form["text1"]
    insert_to_table(data)
    send_to_discord(data)

    required_time = datetime.now() - timedelta(minutes=30)

    # wrong naming: the column "time_of_input" contains the user's inputs
    #               the column "text" contains the TIMESTAMP

    #                           text                                text
    cursor.execute("SELECT time_of_input FROM mydatabase WHERE time_of_input >= ?", (required_time,))
    rows1 = cursor.fetchall()
    con.close()

    return str(rows1)

if __name__ == '__main__':
    app.run()
