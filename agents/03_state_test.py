import sys, os, uuid, json

action = sys.argv[1] if len(sys.argv) > 1 else "write"
file_path = "/tmp/agent_state.txt"

if action == "write":
    session_id = str(uuid.uuid4())
    with open(file_path, "w") as f:
        f.write(session_id)
    print(json.dumps({"action": "write", "id": session_id}))
elif action == "read":
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            print(json.dumps({"action": "read", "id": f.read().strip()}))
    else:
        print(json.dumps({"action": "read", "id": "STATE_LOST"}))
