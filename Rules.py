from collections import Counter

def detect_ddos(data):
    src_ips = [row[2] for row in data]
    counts = Counter(src_ips)

    alerts = []

    for ip, count in counts.items():
        if count > 20:
            alerts.append(f"DDoS Alert: {ip} ({count} packets)")

    return alerts


def detect_port_scan(data):
    # simple logic (demo)
    alerts = []

    src_ips = [row[2] for row in data]
    counts = Counter(src_ips)

    for ip, count in counts.items():
        if count > 50:
            alerts.append(f"Port Scan Suspicion: {ip}")

    return alerts