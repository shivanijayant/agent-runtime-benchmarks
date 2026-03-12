import json, sys

print(json.dumps({"test": "stress", "status": "starting_memory_bloat"}))
sys.stdout.flush()

try:
    # Attempt to allocate ~1GB of RAM rapidly
    bloat = bytearray(1024 * 1024 * 1000) 
    
    # CPU spin
    count = 0
    while count < 10000000:
        count += 1
        
    print(json.dumps({"test": "stress", "status": "survived"}))
except MemoryError:
    print(json.dumps({"test": "stress", "status": "memory_killed"}))
