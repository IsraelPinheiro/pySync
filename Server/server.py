from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import sqlite3
from sqlite3 import Error
import os, json, time, hashlib

server = SimpleXMLRPCServer(("",3000), logRequests=True, allow_none=True)

################ SQLite Connection and management #####################
def createDatabase():
    try:
        conn = sqlite3.connect("PySync.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE "Agents" (
                "id" integer,
                "user"	varchar NOT NULL,
                "password"	varchar(32),
                "agentKey"	varchar(32),
                PRIMARY KEY("id")
            );
        """)
        cursor.execute("""
            INSERT INTO main.Agents ("user", "password", "agentKey")
                VALUES ('User', '5F4DCC3B5AA765D61D8327DEB882CF99', '5EE53A0D21960A1918E3CFC9F1D9356A');
        """)
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def connectDatabase():
    if os.path.exists("PySync.db"):
        conn = None
        try:
            conn = sqlite3.connect("PySync.db")
        except Error as e:
            print(e)
        return conn
    else:
        createDatabase()
        connectDatabase()

def checkUser(databaseConnection, user, password, key):
    if databaseConnection:
        cursor = databaseConnection.cursor()
        password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute(f'SELECT * FROM Agents WHERE user="{user}" and password="{password}" and agentKey = "{key}"')
        register = cursor.fetchone()
        if register:
            print("Usuário localizado")
            databaseConnection.close()
            return True
        else:
            databaseConnection.close()
            return False
    else:
        return False

#######################################################################

class Worker(object):
    pass

def gateway(message, payload):
    action = message["Action"]
    if action=="GetChanges":
        return getChanges(message)

    elif action == "Update":
        return update(message, payload)

    elif action == "Create":
        return create(message, payload)

    elif action == "Delete":
        return delete(message)

    elif action == "RegisterAgent":
        return registerAgent(message)

    elif action == "RegisterUser":
        return registerUser(message)

    else:
        message = {
            "Action":"ServerResponse",
            "Timestamp":time.time(),
            "Status":400
        }
        message = json.dumps(message)
        response = message

    return response

def getChanges(message):
    return (message, None)

def update(message, payload=None):
    if checkUser(connectDatabase(), message["Agent"]["User"]["Email"],message["Agent"]["User"]["Password"],message["Agent"]["Key"]):
        if message["File"]:
            if os.path.isfile(message["File"]["OriginalName"]):
                os.remove("./Files/"+message["File"]["OriginalName"])
                with open("./Files/"+message["File"]["OriginalName"], "wb") as handle:
                    handle.write(payload.data)
                message = {
                    "Action":"ServerResponse",
                    "Timestamp":time.time(),
                    "Status":200
                }

            else:
                message = {
                    "Action":"ServerResponse",
                    "Timestamp":time.time(),
                    "Status":404
                }
        else:
            message = {
                "Action":"ServerResponse",
                "Timestamp":time.time(),
                "Status":400
            }
    else:
        message = {
            "Action":"ServerResponse",
            "Timestamp":time.time(),
            "Status":401
        }

    return (message, None)

def create(message, payload):
    if checkUser(connectDatabase(), message["Agent"]["User"]["Email"],message["Agent"]["User"]["Password"],message["Agent"]["Key"]):
        if message["File"]:
            if not os.path.isfile(message["File"]["OriginalName"]):
                with open("./Files/"+message["File"]["OriginalName"], "wb") as handle:
                    handle.write(payload.data)
                message = {
                    "Action":"ServerResponse",
                    "Timestamp":time.time(),
                    "Status":200
                }

            else:
                message = {
                    "Action":"ServerResponse",
                    "Timestamp":time.time(),
                    "Status":400
                }
        else:
            message = {
                "Action":"ServerResponse",
                "Timestamp":time.time(),
                "Status":400
            }
    else:
        message = {
            "Action":"ServerResponse",
            "Timestamp":time.time(),
            "Status":401
        }

    return (message, None)

def delete(message):
    if checkUser(connectDatabase(), message["Agent"]["User"]["Email"],message["Agent"]["User"]["Password"],message["Agent"]["Key"]):
        if message["File"]:
            if os.path.isfile("./Files/"+message["File"]["OriginalName"]):
                os.remove("./Files/"+message["File"]["OriginalName"])
                message = {
                    "Action":"ServerResponse",
                    "Timestamp":time.time(),
                    "Status":200
                }

            else:
                message = {
                    "Action":"ServerResponse",
                    "Timestamp":time.time(),
                    "Status":404
                }
        else:
            message = {
                "Action":"ServerResponse",
                "Timestamp":time.time(),
                "Status":400
            }

    else:
        message = {
            "Action":"ServerResponse",
            "Timestamp":time.time(),
            "Status":401
        }

    return (message, None)

def registerUser(message):
    key = message["Agent"]["Key"]
    user = message["Agent"]["User"]["Email"]
    password = message["Agent"]["User"]["Password"]
    if key:
        if user and password:
            try:
                conn = connectDatabase()
                conn = sqlite3.connect("PySync.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO main.Agents ('user', 'password', 'agentKey') VALUES ('{User}', '{password}', '{key}');")
                conn.commit()

                message = {
                    "Action":"ServerResponse",
                    "Timestamp":time.time(),
                    "Status":200
                }

            except Error as _:
                message = {
                    "Action":"ServerResponse",
                    "Timestamp":time.time(),
                    "Status":500
                }
            finally:
                if conn:
                    conn.close()
        else:
            message = {
                "Action":"ServerResponse",
                "Timestamp":time.time(),
                "Status":400
            }
    else:
        message = {
            "Action":"ServerResponse",
            "Timestamp":time.time(),
            "Status":400
        }
    return (message, None)

def registerAgent(message):
    return registerUser(message)

if __name__ == '__main__':
    try:
        server.register_function(gateway)
        print('Serving...')
        server.serve_forever()
        
    except KeyboardInterrupt:
        print('Exiting')