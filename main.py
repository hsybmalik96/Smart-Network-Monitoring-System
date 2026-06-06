import subprocess
import time
import sys
import os

# Resolve the project root directory (same folder as this script)
ROOT = os.path.dirname(os.path.abspath(__file__))

def clear_old_data():
    """Clear old database and logs for a fresh start."""
    db_path = os.path.join(ROOT, "network.db")
    log_path = os.path.join(ROOT, "logs", "ids.log")
    
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("[*] Cleared old database.")
        except Exception as e:
            print(f"[!] Could not delete old database: {e}")
            
    if os.path.exists(log_path):
        try:
            os.remove(log_path)
            print("[*] Cleared old logs.")
        except Exception as e:
            pass


def run_sniffer():
    """Start the packet sniffer as a subprocess."""
    return subprocess.Popen(
        [sys.executable, os.path.join(ROOT, "sniffer.py")],
        cwd=ROOT
    )

def run_dashboard():
    """Start the Streamlit dashboard as a subprocess."""
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run",
         os.path.join(ROOT, "Dashboard_UI.py"),
         "--server.headless", "true"],
        cwd=ROOT
    )

if __name__ == "__main__":
    print("[*] Initializing fresh environment...")
    clear_old_data()

    print("[*] Starting packet sniffer...")
    p_sniffer = run_sniffer()

    print("[*] Waiting 3 seconds before launching dashboard...")
    time.sleep(3)

    print("[*] Starting Streamlit dashboard...")
    p_dashboard = run_dashboard()

    print("[✓] Both processes running. Press Ctrl+C to stop.\n")

    try:
        p_sniffer.wait()
        p_dashboard.wait()
    except KeyboardInterrupt:
        print("\n[!] Shutting down...")
        p_sniffer.terminate()
        p_dashboard.terminate()
        print("[✓] Done.")