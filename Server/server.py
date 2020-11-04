from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import os, json, time

server = SimpleXMLRPCServer(("",3000), logRequests=True, allow_none=True)

class Worker(object):
    pass

def gateway(message, payload=None):
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

def update(message, payload):
    if message["File"]:
        if os.path.isfile(message["File"]["OriginalName"]):
            os.remove("Files/"+message["File"]["OriginalName"])
            with open("Files/"+message["File"]["OriginalName"], "wb") as handle:
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

    return (message, None)

def create(message, payload):
    if message["File"]:
        if not os.path.isfile(message["File"]["OriginalName"]):
            with open("Files"+message["File"]["OriginalName"], "wb") as handle:
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

    return (message, None)

def delete(message):
    if message["File"]:
        if os.path.isfile("Files/"+message["File"]["OriginalName"]):
            os.remove("Files/"+message["File"]["OriginalName"])
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

    return (message, None)

def registerAgent(message):
    return (message, None)

def registerUser(message):
    return (message, None)

if __name__ == '__main__':
    try:
        server.register_function(gateway)
        print('Serving...')
        server.serve_forever()
        
    except KeyboardInterrupt:
        print('Exiting')