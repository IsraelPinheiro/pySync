import os, time, socket, json

HOST, PORT = "localhost", 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def update(status, file):
  #data_set = {}
  if status == "Create":
    data = {
      "Action": status, 
      "Agent": {
        "Key": "placeholder",
        "User": {
          "Email": "place@holder.it",
          "Password": "pass"
        }
      },
      "File": {
        "OriginalName": file[0],
        "Size": os.stat(file[0]).st_size
      }
    }
    #data_set = json.dumps(data)
  if status == "Delete":
    data = {
      "Action": status, 
      "Agent": {
        "Key": "placeholder",
        "User": {
          "Email": "place@holder.it",
          "Password": "pass"
        }
      },
      "File": file[0]
    }
    #data_set = json.dumps(data)
  print(data)


def watch_dir(path_to_watch):
  before = dict ([(f, None) for f in os.listdir (path_to_watch)])
  while True:
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    file_added = [f for f in after if not f in before]
    file_removed = [f for f in before if not f in after]
    if file_added: 
      update("Create", file_added)
    if file_removed: 
      update("Delete", file_removed)
    before = after

if __name__ == "__main__":
  path_to_watch = "."
  watch_dir(path_to_watch)
