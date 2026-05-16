import os

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

SOURCE_CHANNELS = [
    int(x.strip())
    for x in os.environ["SOURCE_CHANNELS"].split(",")
]

DEST_CHANNELS = [
    int(x.strip())
    for x in os.environ["DEST_CHANNELS"].split(",")
]

CONTROL_CHAT = int(
    os.environ.get("CONTROL_CHAT", "0")
)

COPY_DELAY = float(
    os.environ.get("COPY_DELAY", "1")
)
