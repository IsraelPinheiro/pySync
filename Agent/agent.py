from xmlrpc.client import ServerProxy, Binary
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os, json
 
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
        print("Arquivo Excluído - "+event.src_path)

    def on_modified(self, event):
        print("Arquivo Modificado - "+event.src_path)
            
    def on_moved(self, event):
        print("Arquivo Movido - "+event.src_path)

    def snapshot(self):
        pass

if __name__ == "__main__":
    proxy = ServerProxy('http://localhost:3000')
    #TODO Separar Thread do Watcher
    #TODO Disparar thread com 
    watcher = Watcher()