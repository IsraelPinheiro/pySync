from xmlrpc.client import ServerProxy, Binary
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os, json, threading, argparse, hashlib, sqlite3

################ Argparser ################
parser = argparse.ArgumentParser()

parser.add_argument("username", help="Your Username", type=str)
parser.add_argument("password", help="User Password", type=str)
parser.add_argument("--key", help="Agent Key", type=str)
args = parser.parse_args()

USERNAME = args.username
PASSWORD = hashlib.md5(args.password.encode()).hexdigest()

#Check Agent key and generate one if not exists
if args.key:
    AGENT_KEY = args.key.upper()
else:
    if os.path.isfile("agent.key"):
        with open("agent.key") as f:
            AGENT_KEY = f.readline()
    else:
        AGENT_KEY = hashlib.md5(str(time.time()).encode()).hexdigest().upper()
        with open("agent.key","w+") as f:
            f.write(AGENT_KEY)

print(f"Accessing as {USERNAME} using agent {AGENT_KEY}")

###########################################

class Watcher(object):
    def __init__(self):
        observer = Observer()
        event_handler = EventHandler()
        path = "."
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        self.snapshot()

    def on_created(self, event):
        time.sleep(0.2)
        message = {
            "Action":"Create",
            "Timestamp":time.time(),
            "Agent":{
                "Key":AGENT_KEY,
                "User":{
                    "Email":USERNAME,
                    "Password":PASSWORD
                }
            },
            "File":{
                "OriginalName": os.path.basename(event.src_path),
                "Size": os.path.getsize(event.src_path)
            }

        }

        with open(event.src_path, "rb") as handle:
            payload = Binary(handle.read())

        awnser = proxy.gateway(message, payload)
        print(awnser)
        
    def on_deleted(self, event):
        message = {
            "Action":"Delete",
            "Timestamp":time.time(),
            "Agent":{
                "Key":AGENT_KEY,
                "User":{
                    "Email":USERNAME,
                    "Password":PASSWORD
                }
            },
            "File": os.path.basename(event.src_path)

        }

        with open("files.json", "r") as openfile:
            data = json.load(openfile)
        data.pop(os.path.basename(event.src_path))
        with open("files.json", "w") as outfile: 
            json.dump(data, outfile)

        awnser = proxy.gateway(message, None)
        print(awnser)

    def on_modified(self, event):
        pass
            
    def on_moved(self, event):
        pass

    def snapshot(self):
        pass

def Watch_files():
    with open("files.json", "r") as openfile:
        data = json.load(openfile)
    while True:
        time.sleep(1)
        dir_files = dict ([(f, None) for f in os.listdir()])
        for file in dir_files:
            data.update({
                file: os.stat(file).st_mtime
            })
            if os.stat(file).st_mtime > data[file] and "dir_files" not in file and "agent" not in file:
                time.sleep(0.2)
                
                message = {
                    "Action":"Delete",
                    "Timestamp":time.time(),
                    "Agent":{
                        "Key":AGENT_KEY,
                        "User":{
                            "Email":USERNAME,
                            "Password":PASSWORD
                        }
                    },
                    "File": file

                }

                awnser = proxy.gateway(message, None)
                print(awnser)

            with open("files.json", "w") as outfile: 
                json.dump(data, outfile)

if __name__ == "__main__":
    try:
        #Create files.json if not exists
        if not os.path.exists("files.json"):
            with open("files.json","w+") as f:
                f.write("{}")

        print("Connecting to remote server")
        proxy = ServerProxy('http://localhost:3000', allow_none=True)

        print("Initializing monitoring threads")
        threadWatcher = threading.Thread(target=Watcher,args=())
        threadWatcher.start()
        threadWatchFiles = threading.Thread(target=Watch_files,args=())
        threadWatchFiles.start()

        print("Running...")

    except (KeyboardInterrupt, SystemExit):
        threadWatcher.join()
        threadWatchFiles.join()
        exit(0)
        print('Exiting')