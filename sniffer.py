from scapy.all import sniff
from database.db import insert_packet
from email_alerts import send_alert
from Rules import detect_ddos, detect_port_scan
import time
import logging
import os

# ─── Setup ────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/ids.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

# ─── State for alert throttling (avoid email spam) ────────────
_sent_alerts = set()          # tracks which alert messages were already emailed
_packet_buffer = []           # rolling buffer to run detection on
BUFFER_SIZE = 100             # run detection every N packets
_packet_count = 0             # track total packets for detection intervals

def process_packet(packet):
    global _packet_buffer, _packet_count

    try:
        if packet.haslayer("IP"):
            src = packet["IP"].src
            dst = packet["IP"].dst
            t   = time.strftime("%H:%M:%S")

            print(f"  {t}  {src} → {dst}")
            insert_packet(t, src, dst)
            logging.info(f"{src} -> {dst}")

            # Add to rolling buffer
            _packet_buffer.append((None, t, src, dst))
            if len(_packet_buffer) > BUFFER_SIZE:
                _packet_buffer = _packet_buffer[-BUFFER_SIZE:]

            # Run detection every BUFFER_SIZE packets
            _packet_count += 1
            if _packet_count % BUFFER_SIZE == 0:
                _run_detection()

    except Exception as e:
        logging.error(str(e))


def _run_detection():
    """Run DDoS + Port Scan detection and send email alerts for new threats."""
    alerts = detect_ddos(_packet_buffer) + detect_port_scan(_packet_buffer)
    for alert in alerts:
        if alert not in _sent_alerts:
            _sent_alerts.add(alert)
            logging.warning(f"ALERT: {alert}")
            print(f"\n[🚨 ALERT] {alert}")
            # Determine subject line
            subject = "DDoS Attack Detected" if "DDoS" in alert else "Port Scan Detected"
            msg = f"NetIDS Alert: {subject}\n\n{alert}"
            send_alert(msg)


def start_sniffer():
    print("=" * 50)
    print("  🛡️  Smart Network IDS — Packet Sniffer")
    print("=" * 50)
    print("  Capturing live traffic... Press Ctrl+C to stop.\n")
    sniff(prn=process_packet, store=False)


if __name__ == "__main__":
    start_sniffer()