import sqlite3
def getConnection():
    conn = sqlite3.connect('form_filling_app.db')
    if conn:
        print("Connection successful")
    else:
        print("Connection failed")
        exit()
    query = '''
    CREATE TABLE IF NOT EXISTS users (
        userID INT PRIMARY KEY,
        firstname VARCHAR(20) NOT NULL,
        lastname VARCHAR(20) NOT NULL,
        DOB DATE NOT NULL,
        phone VARCHAR(50) NOT NULL UNIQUE,
        gender VARCHAR(6) NOT NULL
    );
    '''
    conn.execute(query)
    conn.commit()
    return conn

def insert(conn, userDetails):
    maxID = conn.execute("SELECT MAX(userID) FROM users").fetchone()[0]
    if not maxID:
        maxID = 0
    query = '''
    INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);
    '''
    queryData = (maxID + 1, userDetails['firstname'], userDetails['lastname'], userDetails['dob'], userDetails['phone'], userDetails['gender'])
    if conn.execute(query, queryData):
        conn.commit()
        return maxID+1
    return False

def fetchRecords(conn, userID = None):
    query = "SELECT * FROM users " + ("WHERE userID = " + str(userID) if userID else "") + ";"
    return conn.execute(query).fetchall()