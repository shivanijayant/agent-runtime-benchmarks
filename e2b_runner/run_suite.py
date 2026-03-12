from e2b import Sandbox
import time
import os

def run_tests():
    print("--- Starting E2B Benchmark Suite ---")
    
    # 1. Dynamically find the absolute paths on your machine
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    REPO_ROOT = os.path.dirname(SCRIPT_DIR)
    
    # 2. Boot the microVM
    t0 = time.time()
    sandbox = Sandbox.create()
    print(f"[Infrastructure] Sandbox booted in {time.time() - t0:.2f}s")
    
    # 3. Upload assets using the absolute paths
    data_file = os.path.join(REPO_ROOT, "data", "transactions.csv")
    sandbox.files.write("transactions.csv", open(data_file, "rb").read())
    
    for script in ["01_baseline.py", "02_stress_test.py", "03_state_test.py"]:
        script_file = os.path.join(REPO_ROOT, "agents", script)
        sandbox.files.write(script, open(script_file, "rb").read())
        
    # 4. Install dependencies
    sandbox.commands.run("pip install pandas")
    
    # Run Baseline
    print("\n[Test 1] Baseline Execution")
    out = sandbox.commands.run("python 01_baseline.py")
    print(out.stdout)
    
    # Run Stress Test
    print("\n[Test 2] Stress Test (1GB RAM + CPU Spin)")
    out = sandbox.commands.run("python 02_stress_test.py")
    print(out.stdout)
    
    # Run State Test (Write, wait, Read)
    print("\n[Test 3] State Persistence")
    sandbox.commands.run("python 03_state_test.py write")
    time.sleep(2)
    out = sandbox.commands.run("python 03_state_test.py read")
    print(out.stdout) 
    
    # Clean up
    sandbox.kill()

if __name__ == "__main__":
    run_tests()
