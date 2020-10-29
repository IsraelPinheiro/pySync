import os, time
path_to_watch = "."
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while True:
  time.sleep (5)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  file_added = [f for f in after if not f in before]
  file_removed = [f for f in before if not f in after]
  if file_added: 
    print ("file_added: ", ", ".join (file_added))
  if file_removed: 
    print ("file_removed: ", ", ".join (file_removed))
  before = after