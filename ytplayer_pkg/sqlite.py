import sqlite3

def createTable():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print("Opened database successfully")	
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='PLAYLIST' ''')

    #if the count is 1, then table exists
    if c.fetchone()[0] == 1: 
        print('Table exists.')
    else:
        print("Create table PLAYLIST")
        conn.execute('''CREATE TABLE PLAYLIST
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME           TEXT    NOT NULL,
                URL           TEXT    NOT NULL,
                USERID           CHAR(50));''')

        print("Table created successfully")

        conn.close()
    
def savePlaylist(playlist):
    createTable()
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")

    print("Truncate table PLAYLIST")
    conn.execute("DELETE FROM PLAYLIST")
    conn.commit()
    
    print("Insert playlist to DB")
    for item in playlist:
        print("item", item.name, item.url, item.userId)
        conn.execute("INSERT INTO PLAYLIST (NAME, URL, USERID) VALUES ('{}', '{}', '{}')".format(item.name, item.url, item.userId))

    conn.commit()
    print("Records created successfully")

    conn.close()
    
def getPlaylist():
    try:
        conn = sqlite3.connect('test.db')
        print("Opened database successfully")

        cursor = conn.execute("SELECT NAME, URL, USERID from PLAYLIST")
        for row in cursor:
            print("NAME = ", row[0])
            print("URL = ", row[1])
            print("USERID = ", row[2], "\n")

        print("Operation done successfully")
        conn.close()
        return cursor
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        