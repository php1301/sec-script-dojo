from pathlib import Path 
import os 
import sys 
import csv 
import string 
import re
import urllib.parse as up
import subprocess
from collections import Counter

LAB5_DIR = Path(__file__).resolve().parent / "lab5"
LAB5_DIR.mkdir(exist_ok=True, parents=True)
os.chdir(LAB5_DIR)

# E24: Print lines suggesting SQLi (URL-decode first) — IQ-102
with open('E24_access.log') as f:
    FIELDS = ["ip", "ident", "user", "ts", "tz", "request", "status", "bytes"]
    patterns_24 = [
        # re.compile(r'\bselect\b.+?\bfrom\b', re.I)
        re.compile(r'\/login\?user=(admin|root)', re.I),
        re.compile(r'select.+?from', re.I),
        re.compile(r'union|sleep|drop', re.I)
    ]   
    for idx, row in enumerate(csv.DictReader(f, delimiter=" ", quotechar='"', fieldnames=FIELDS), start=1):
        for pattern in patterns_24:
            q_param = row["request"].split()[1]
            # decoded = up.unquote_plus(q_param)
            # print(decoded)
            m = re.search(pattern, q_param)
            print(m)
# Method 2: Use a list of known SQLi signatures
# with open('E24_access.log') as f:
#     SIGS = ["union select", "' or '", " or 1=1", " and 1=1", "'--",
#             "sleep(", "drop table", "@@version", "information_schema"]

#     decoded = up.unquote_plus(up.unquote_plus(url)).lower()
#     for sig in SIGS:
#         if sig in decoded:
#             print(row["ip"], row["status"], row["bytes"], decoded)
#             break


cmd_24 = r'''
        grep -n -i -E \
        -e "select.+from" \
        -e "union|sleep|drop" \
        -e "1=1" \
        -e "/login\?user=(admin|root)" "$0"
'''
r = subprocess.run(
    ["bash", "-c", cmd_24, "E24_access.log"],
    capture_output=True,
    check=True,
    timeout=15
)
print(r.stdout.decode())
# E25: Most active source IP in Netflow (flows vs bytes) — IQ-103
print('E25: Most active source IP in Netflow (flows vs bytes) — IQ-103')
with open('E25_E31_netflow.csv') as f:
    by_ip = Counter()
    by_byte = Counter()
    for idx, row in enumerate(csv.DictReader(f), start=1):
        # print(row, idx)
        by_ip[row["src_ip"]] += 1
        by_byte[row["src_ip"]] += int(row["bytes"])
    [print(f"By IP {k}: {v}") for k, v in by_ip.items()]
    [print(f"By bytes {k}: {v}") for k, v in by_byte.items()]
    print(f"Top by flows {by_ip.most_common(1)}")
    print(f"Top by bytes {by_byte.most_common(1)}")

# E26: Events per minute (time bucketing)
# E27: Brute-force candidates: 3+ failures with first and last time
# E28: Correlate two logs with a hashmap of lists — IQ-101
# E29: Enrich alerts with hostnames (UNKNOWN if missing)
# E30: Suspicious success: fail, then ok, per user
# E31: Port-scan detection: unique destinations per source
    