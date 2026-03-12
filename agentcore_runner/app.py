from bedrock_agentcore import BedrockAgentCoreApp
import subprocess, json

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    test_name = payload.get("test", "baseline")
    
    if test_name == "baseline":
        out = subprocess.run(["python", "agents/01_baseline.py"], capture_output=True, text=True)
        return {"result": out.stdout, "errors": out.stderr}
        
    elif test_name == "stress":
        out = subprocess.run(["python", "agents/02_stress_test.py"], capture_output=True, text=True)
        return {"result": out.stdout, "errors": out.stderr}
        
    elif test_name == "state_write":
        out = subprocess.run(["python", "agents/03_state_test.py", "write"], capture_output=True, text=True)
        return {"result": out.stdout, "errors": out.stderr}
        
    elif test_name == "state_read":
        out = subprocess.run(["python", "agents/03_state_test.py", "read"], capture_output=True, text=True)
        return {"result": out.stdout, "errors": out.stderr}

if __name__ == "__main__":
    app.run()
