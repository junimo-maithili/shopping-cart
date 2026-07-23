import sqlite3
import routes
import importlib

# Function to update a row with certain information

# Function to update the database
def updateDb(uuid, budgetData, priceData, fbId):

    print("budget =", repr(budgetData))

    try:
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()
    

        # Create a table for users
        cursor.execute("CREATE TABLE IF NOT EXISTS FIREBASEIDS (Id INTEGER PRIMARY KEY, FirebaseId Varchar(50))")

        if fbId:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM FIREBASEIDS WHERE FirebaseId = ?)", (fbId,))
            result = cursor.fetchone()

            if result == (0,):
                print("Adding a FireBase Id!")
                cursor.execute("INSERT INTO FIREBASEIDS (FirebaseId) VALUES (?)", (fbId,))
        new_id = cursor.lastrowid



        # Create a table for devices
        cursor.execute("CREATE TABLE IF NOT EXISTS DEVICES (Id INT, DeviceUuid Varchar(50))")

        # Check to see if the device is already in the table
        #if uuid:
        uuid = str(uuid)
        cursor.execute("SELECT EXISTS (SELECT 1 FROM DEVICES WHERE DeviceUuid = ?)", (uuid,))
        result = cursor.fetchone()

        # If ID doesn't exist, make a new entry
        if result == (0,):
            print(uuid)
            print("Adding a new UUID!")
            cursor.execute("INSERT INTO DEVICES (Id, DeviceUuid) VALUES (?,?)", (new_id, uuid))


        # Create a table for other info (budget, price)
        cursor.execute("CREATE TABLE IF NOT EXISTS USERINFO (Id INT, Budget VARCHAR(25), Price VARCHAR(25))")
        cursor.execute("SELECT EXISTS (SELECT 1 FROM USERINFO WHERE Id = ?)", (new_id,))
        result = cursor.fetchone()

        if result == (0,):
            cursor.execute("INSERT INTO USERINFO (Id) VALUES (?)", (new_id,))

        # Put budget in table
        if budgetData:
            importlib.reload(routes)
            budgetData = str(budgetData) # find a more efficient way to do this in one line
            print("trying to add budget: " + budgetData)
        cursor.execute("UPDATE USERINFO SET Budget = ? WHERE Id = ?", (budgetData, new_id))            

        # Put price in table
        if priceData:
            importlib.reload(routes)
            priceData = str(priceData) # find a more efficient way to do this in one line
            print("trying to add price: " + priceData)
        cursor.execute("UPDATE USERINFO SET Price = ? WHERE Id = ?", (priceData, new_id))            


        query = """SELECT * FROM USERINFO"""
        cursor.execute("SELECT * FROM FIREBASEIDS")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred -', error)

    finally:
        if sqliteConnection:
            sqliteConnection.commit()
            sqliteConnection.close()
            print('SQLite connection closed')


# is it bad to have two cursors
def sendInfo(fbId):
    try:
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT * FROM FIREBASEIDS WHERE FirebaseId = ?", (fbId,))
        result = cursor.fetchone()
        if not result:
            return None
        
        new_id = result[0]

        cursor.execute("SELECT * FROM USERINFO WHERE Id = ?", (new_id,)) # change this table name maybe
        result = cursor.fetchone()
        cursor.close()

        return result
        

    except sqlite3.Error as error:
        print('Error occurred -', error)

    finally:
        if sqliteConnection:
            sqliteConnection.commit()
            sqliteConnection.close()
            print('SQLite connection closed')
