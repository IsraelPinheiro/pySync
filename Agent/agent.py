from xmlrpc.client import ServerProxy, Binary
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os, json, threading
 
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
            "Timestamp":1604061231.0383,
            "Agent":{
                "Key":"6C19A781148814833ED25840B7A07BA7",
                "User":{
                    "Email":"usuario01@pysync.com",
                    "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0"
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
            "Timestamp":1604061231.0383,
            "Agent":{
                "Key":"6C19A781148814833ED25840B7A07BA7",
                "User":{
                    "Email":"usuario01@pysync.com",
                    "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0"
                }
            },
            "File": os.path.basename(event.src_path)

        }

        with open("dir_files.json", "r") as openfile:
            data = json.load(openfile)
        data.pop(os.path.basename(event.src_path))
        with open("dir_files.json", "w") as outfile: 
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
    with open("dir_files.json", "r") as openfile:
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
                    "Timestamp":1604061231.0383,
                    "Agent":{
                        "Key":"6C19A781148814833ED25840B7A07BA7",
                        "User":{
                            "Email":"usuario01@pysync.com",
                            "Password":"D1A5FF8DBEEDAA3406368724EBBD3CB0"
                        }
                    },
                    "File": file

                }

                awnser = proxy.gateway(message, None)
                print(awnser)

            with open("dir_files.json", "w") as outfile: 
                json.dump(data, outfile)

if __name__ == "__main__":
    proxy = ServerProxy('http://localhost:3000', allow_none=True)
    threading.Thread(target=Watcher,args=()).start()
    threading.Thread(target=Watch_files,args=()).start()