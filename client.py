import os, time, socket, json, threading

HOST, PORT = "localhost", 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_to_server(data):
  data_set = json.dumps(data)
  try:
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data_set,encoding="utf-8"))

    response = sock.recv(1024)
    response = response.decode("utf-8")

    if response["Status"] != 200:
      print("Server error")

  finally:
    sock.close()

def update(status, file):
  data = {
    "Action": status, 
    "Agent": {
      "Key": "placeholder",
      "User": {
        "Email": "place@holder.it",
        "Password": "pass"
      }
    },
  }

  # this delay is needed to the algorithm can get the file size
  time.sleep(0.2)

  if status == "Create":
    data.update({
      "File": {
        "OriginalName": file[0],
        "Size": os.stat(file[0]).st_size
      },
    })
  if status == "Delete":
    data.update({
      "File": file[0]
    })

  threading.Thread(target=send_to_server,args=(data,)).start()

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
