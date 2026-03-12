import sys, json, uuid, os

STATE_FILE = "/tmp/state.json"

if sys.argv[1] == "write":
    uid = str(uuid.uuid4())
    with open(STATE_FILE, "w") as f:
        json.dump({"id": uid}, f)
    print(json.dumps({"action": "write", "id": uid}))

elif sys.argv[1] == "read":
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
        print(json.dumps({"action": "read", "id": data["id"]}))
    else:
        print(json.dumps({"action": "read", "id": "null"}))
