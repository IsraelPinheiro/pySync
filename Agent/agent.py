from xmlrpc.client import ServerProxy, Binary
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os
 
class Watcher(object):
    def __init__(self):
        observer = Observer()
        event_handler = EventHandler()
        path = "Agent"
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
        if os.path.isfile(event.src_path):
            print("Arquivo Criado - "+event.src_path)
        
    def on_deleted(self, event):
        if os.path.isfile(event.src_path):
            print("Arquivo Excluído - "+event.src_path)

    def on_modified(self, event):
        if os.path.isfile(event.src_path):
            print("Arquivo Modificado - "+event.src_path)
            
    def on_moved(self, event):
        if os.path.isfile(event.src_path):
            print("Arquivo Movido - "+event.src_path)

    def snapshot(self):
        pass




if __name__ == "__main__":
    proxy = ServerProxy('http://localhost:3000')
    #TODO Separar Thread do Watcher
    #TODO Disparar thread com 
    watcher = Watcher()