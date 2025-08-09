import psycopg2
import psycopg2.extras
from tkinter import *
from tkinter import messagebox
import configparser




def connect_to_db():

    config = configparser.ConfigParser()
    config.read('config.ini')  # Make sure this file is in same folder as main.py


    db_params = config['postgresql']
    
    conn = psycopg2.connect(
    host=db_params['host'],
    dbname=db_params['database'],
    user=db_params['user'],
    password=db_params['password'],
    port=db_params['port']
    )
    cur = conn.cursor()

    create_script1 = '''CREATE TABLE IF NOT EXISTS players(
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    age INT NOT NULL,
    type VARCHAR(40)
    )'''
    cur.execute(create_script1)

    create_script2 = '''CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(40) NOT NULL UNIQUE,
    password VARCHAR(40) NOT NULL,
    role VARCHAR(20) NOT NULL,
    player_id INT UNIQUE,
    FOREIGN KEY (player_id) REFERENCES
    players (id)
    )'''
    cur.execute(create_script2)

    create_script3 = '''CREATE TABLE IF NOT EXISTS matches(
    id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL DEFAULT CURRENT_DATE,
    opponent VARCHAR(20),
    location VARCHAR(20),
    match_type VARCHAR(20)
    )'''
    cur.execute(create_script3)

    create_script4 = '''CREATE TABLE IF NOT EXISTS batting_stats(
    id SERIAL PRIMARY KEY,
    player_id INT,
    match_id INT,
    runs_scored INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    dismissal BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (player_id) REFERENCES
    players (id),
    FOREIGN KEY (match_id) REFERENCES
    matches (id)
    )'''
    cur.execute(create_script4)

    create_script5 = '''CREATE TABLE IF NOT EXISTS bowling_stats(
    id SERIAL PRIMARY KEY,
    player_id INT,
    match_id INT,
    balls_bowled INT DEFAULT 0,
    runs_conceded INT DEFAULT 0,
    wickets INT DEFAULT 0,
    maidens INT DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES
    players (id),
    FOREIGN KEY (match_id) REFERENCES
    matches (id)
    )'''
    cur.execute(create_script5)
    
    create_script6 = '''CREATE TABLE IF NOT EXISTS fielding_stats(
    id SERIAL PRIMARY KEY,
    player_id INT,
    match_id INT,
    catches INT DEFAULT 0,
    run_outs INT DEFAULT 0,
    stumpings INT DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES
    players (id),
    FOREIGN KEY (match_id) REFERENCES
    matches (id)
    )'''
    cur.execute(create_script6)


    conn.commit()
    return conn



def validate_login(conn,username,password):
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username =%s AND password =%s",(username,password))
    result = cur.fetchone()
    if result:
        return result[0]
    return None


def player_name(conn,username,password):
    cur=conn.cursor()
    cur.execute("SELECT p.id FROM users u JOIN players p ON u.player_id = p.id WHERE u.username=%s AND u.password=%s",(username,password))
    result = cur.fetchone()
    if result:
        return result[0]   # just return the name string
    return None


def add_user_and_player(conn,name,age,player_type,username,password,role):
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO players (name, age, type) VALUES (%s, %s, %s) RETURNING id",
            (name, age, player_type)
        )
        player_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO users (username, password, role, player_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (username, password, role, player_id)
            
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error","Failure in inserting data")
        return False
        