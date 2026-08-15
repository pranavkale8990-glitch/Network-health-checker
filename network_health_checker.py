"""
Network Device Health Checker
------------------------------
A simple automation script that checks whether a list of network devices
(IP addresses or hostnames) is UP or DOWN, and logs the result with a
timestamp to a CSV report.

Why this project matters (for interviews):
This is a small version of what EMS (Element Management System) / SMO
(Service Management and Orchestration) automation does in telecom networks:
instead of a human manually checking hundreds of devices one by one, a
script checks them automatically and produces a report.

How it works:
1. Reads a list of devices from devices.txt (one IP/hostname per line).
2. Pings each device using the system's ping command.
3. Records whether each device is UP or DOWN, and how long the ping took.
4. Saves everything to a timestamped CSV log file (health_log.csv).
5. Prints a clean summary to the console.

Usage:
    python network_health_checker.py
"""

import subprocess       # lets us run the system "ping" command from Python
import platform         # lets us detect if we're on Windows or Linux/Mac
import csv               # for writing structured results to a .csv file
import datetime          # for timestamping every check
import os


DEVICE_FILE = "devices.txt"
LOG_FILE = "health_log.csv"


def load_devices(filename):
    """Read the list of devices (IPs or hostnames) from a text file."""
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found. Create it with one IP/hostname per line.")
        return []

    with open(filename, "r") as f:
        # strip() removes whitespace/newlines, skip blank lines and comments
        devices = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return devices


def ping_device(device):
    """
    Ping a single device once and return a tuple: (status, response_time_ms).
    Works on both Windows ('-n') and Linux/Mac ('-c') since the ping
    command flags differ between operating systems.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", device]

    start_time = datetime.datetime.now()
    try:
        # timeout=5 makes sure a dead device doesn't hang the script forever
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        elapsed_ms = round((datetime.datetime.now() - start_time).total_seconds() * 1000, 1)

        if result.returncode == 0:
            return "UP", elapsed_ms
        else:
            return "DOWN", None

    except subprocess.TimeoutExpired:
        return "DOWN", None
    except FileNotFoundError:
        # happens if the 'ping' command isn't available on this system
        print("Error: 'ping' command not found on this system. "
              "On Windows/Mac/most Linux distros it's built in; "
              "on minimal Linux installs, install it with: sudo apt install iputils-ping")
        raise SystemExit(1)


def check_all_devices(devices):
    """Ping every device in the list and collect the results."""
    results = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for device in devices:
        status, response_time = ping_device(device)
        results.append({
            "timestamp": timestamp,
            "device": device,
            "status": status,
            "response_time_ms": response_time if response_time is not None else "",
        })
        # live feedback in the console as each device is checked
        symbol = "✅" if status == "UP" else "❌"
        rt_display = f"{response_time} ms" if response_time is not None else "no response"
        print(f"{symbol}  {device:<20} {status:<6} {rt_display}")

    return results


def save_results(results, filename):
    """Append the results to a CSV log file (creates it if it doesn't exist)."""
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "device", "status", "response_time_ms"])
        if not file_exists:
            writer.writeheader()   # only write the header row once
        writer.writerows(results)


def print_summary(results):
    """Print a short summary: how many devices are up vs down."""
    total = len(results)
    up_count = sum(1 for r in results if r["status"] == "UP")
    down_count = total - up_count

    print("\n--- Summary ---")
    print(f"Total devices checked : {total}")
    print(f"UP                    : {up_count}")
    print(f"DOWN                  : {down_count}")

    if down_count > 0:
        down_devices = [r["device"] for r in results if r["status"] == "DOWN"]
        print(f"Devices needing attention: {', '.join(down_devices)}")


def main():
    devices = load_devices(DEVICE_FILE)
    if not devices:
        return

    print(f"Checking {len(devices)} device(s)...\n")
    results = check_all_devices(devices)
    save_results(results, LOG_FILE)
    print_summary(results)
    print(f"\nFull results appended to '{LOG_FILE}'")


if __name__ == "__main__":
    main()
