import os
import signal
import sqlite3
import subprocess
from datetime import datetime

# CONFIGURATION
DB_PATH = os.path.expanduser("~/kesselflow/db/kessel_state.db")
TARGET_PROCESSES = ["Void_Encoder", "browserbird", "miner_service"]

def debug_log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [WITCH_HUNTER] {msg}")

def neutralize_targets():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    found_threats = 0
    
    for target in TARGET_PROCESSES:
        try:
            # Search for PIDs
            pids = subprocess.check_output(["pgrep", "-f", target]).decode().split()
            
            for pid in pids:
                # Neutralize
                os.kill(int(pid), signal.SIGKILL)
                msg = f"Neutralized {target} (PID: {pid})"
                cursor.execute("INSERT INTO audit_logs (status, message) VALUES ('THREAT_KILL', ?)", [msg])
                debug_log(msg)
                found_threats += 1
                
        except subprocess.CalledProcessError:
            # pgrep returns non-zero if no process is found; ignore.
            continue
        except Exception as e:
            debug_log(f"Error neutralizing {target}: {str(e)}")

    if found_threats == 0:
        debug_log("Sweep complete: No unauthorized threads detected.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    neutralize_targets()
