import prodigy
from prodigy.components.db import Database
from prodigy.components.db import connect


db = connect()

all_annotations = db.datasets
all_sessions = db.sessions

print("Names of all Datasets:", all_annotations)
print("Amount datasets:", len(db))
print("All sessions:", all_sessions)