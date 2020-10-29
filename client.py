import os, time

def update(status, file):
  print("status: ", status, "file: ", file)

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
