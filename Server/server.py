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
    with open("Server/filename.txt", "wb") as handle:
        handle.write(payload.data)

    message = {
        "Action":"ServerResponse",
        "Timestamp":time.time(),
        "Status":200
    }

    return (message, None)

def create(message, payload):
    return (message, None)

def delete(message):
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