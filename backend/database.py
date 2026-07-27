import sqlite3
import routes
import importlib

# Function to update a row with certain information

# Function to update the database
def updateDb(uuid, budgetData, priceData, fbId):
    print("Updating Db!")

    try:
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()

        # Create a table for users
        cursor.execute("CREATE TABLE IF NOT EXISTS FIREBASEIDS (Id INTEGER PRIMARY KEY AUTOINCREMENT, FirebaseId Varchar(50))")
        # Create a table for devices
        cursor.execute("CREATE TABLE IF NOT EXISTS DEVICES (Id INTEGER PRIMARY KEY AUTOINCREMENT, DeviceUuid Varchar(50))")
        # Create a table for other info (budget, price)
        cursor.execute("CREATE TABLE IF NOT EXISTS USERINFO (Id INTEGER PRIMARY KEY, Budget VARCHAR(25), Price VARCHAR(25))")

        cursor.execute("SELECT Id FROM DEVICES WHERE DeviceUuid = ?", (uuid,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                "INSERT INTO DEVICES (DeviceUuid) VALUES (?)",
                (uuid,)
            )
            new_id = cursor.lastrowid
        else:
            new_id = row[0]

       
        # Check to see if the device is already in the table
        #if uuid:
        if uuid is not None:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM DEVICES WHERE DeviceUuid = ?)", (uuid,))
            result = cursor.fetchone()

            # If ID doesn't exist, make a new entry
            if result == (0,):
                cursor.execute("INSERT INTO DEVICES (Id, DeviceUuid) VALUES (?,?)", (new_id, uuid))




        print("DEVICE ID:", new_id)

        cursor.execute("SELECT * FROM USERINFO")
        print("CURRENT USERINFO:", cursor.fetchall())

       
        cursor.execute("SELECT EXISTS (SELECT 1 FROM USERINFO WHERE Id = ?)", (new_id,))
        result = cursor.fetchone()

        print("USERINFO EXISTS RESULT:", result)



        if result == (0,):
            cursor.execute("INSERT INTO USERINFO (Id) VALUES (?)", (new_id,))

        # Put budget in table
        if budgetData is not None:
            budgetData = str(budgetData)
            cursor.execute("UPDATE USERINFO SET Budget = ? WHERE Id = ?", (budgetData, new_id))            

        # Put price in table
        if priceData is not None:
            priceData = str(priceData)
            print("trying to add price: " + priceData)
            cursor.execute("UPDATE USERINFO SET Price = ? WHERE Id = ?", (priceData, new_id))            


        query = """SELECT * FROM USERINFO"""
        cursor.execute(query)

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
def sendInfo(uuid):
    try:
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT * FROM FIREBASEIDS WHERE Uuid = ?", (uuid,))
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
