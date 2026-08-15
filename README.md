# Network Device Health Checker

A Python automation script that checks whether a list of network devices
(IP addresses or hostnames) is UP or DOWN, and logs the results with
timestamps to a CSV report.

## Why this project

Telecom EMS (Element Management System) / SMO (Service Management and
Orchestration) software automatically monitors hundreds of network devices
so engineers don't have to check them manually. This project is a small,
working version of that same idea — built to demonstrate Python scripting
and basic networking concepts.

## How it works

1. `devices.txt` holds the list of devices to check (one per line).
2. The script pings each device using the system `ping` command.
3. Each result (UP/DOWN, response time, timestamp) is saved to `health_log.csv`.
4. A summary is printed to the console, flagging any device that's DOWN.

## How to run it

1. Make sure Python 3 is installed.
2. Edit `devices.txt` and add the IPs/hostnames you want to monitor.
3. Run:
   ```
   python network_health_checker.py
   ```
4. Check `health_log.csv` for the full history of results — every run appends
   new rows, so over time you build a log of device uptime.

## Example output

```
Checking 4 device(s)...

✅  8.8.8.8               UP     18.2 ms
✅  1.1.1.1               UP     14.7 ms
✅  google.com            UP     22.1 ms
❌  192.168.1.1           DOWN   no response

--- Summary ---
Total devices checked : 4
UP                    : 3
DOWN                  : 1
Devices needing attention: 192.168.1.1

Full results appended to 'health_log.csv'
```

## Possible extensions (good "what would you add next" answers)

- Run on a schedule (e.g. every 5 minutes) using Python's `schedule` library
  or a cron job, so it monitors continuously instead of one-off checks.
- Send an email or Slack alert automatically when a device goes DOWN.
- Build a simple Flask web dashboard to visualize device status and history.
- Read the device list from a database instead of a text file.

## How to talk about this in an interview

- **What it does:** "It automatically pings a list of network devices and
  logs whether each one is up or down, instead of checking them manually."
- **Why you built it:** "I wanted a hands-on project that mirrors what
  EMS/SMO automation does — monitoring network elements — since that's
  close to what this internship focuses on."
- **What you learned:** subprocess handling, reading/writing files, basic
  error handling (timeouts), and structuring data with CSV.
- **What you'd improve:** mention 1-2 items from "Possible extensions"
  above — this shows you're already thinking beyond the basic version.
