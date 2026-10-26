import re
import subprocess
import csv 
from collections import Counter

# 14: Timestamp and IP from Apache logs (IQ-100)

# pattern14 = r'^(1-9){1-3}\.((\d){1-3}\.)\1{2}(0-9){1-4}(\s-)\2{2}$'
# def map_header(line):
#     if len(line) != len(FIELDS):
#         return []
#     else:
#         return zip(FIELDS, lines)
with open('lab3/access.log') as f:
    FIELDS = ["ip", "ident", "user", "ts", "tz", "method", "path", "proto", "status", "bytes"]
    lines = f.readlines()
    for line in lines:
        if not line.split(): # skip blank line
            continue
        if len(line.split()) != 10:
            print("Corrupted")
        else:
            row = dict(zip(FIELDS, line.split()))
            print(f"Timestamp {row["ts"].lstrip("[")} IP {row["ip"]}")

print("14. use bash")
script_14 = r'''
    awk 'NF==10 {print "IP: " $1 " at " substr($4, 2)}' "$0";
    awk 'NF==10 {print $1, substr($4, 2)}' "$0";
'''
r = subprocess.run(
    ["bash", "-c", script_14, "./lab3/access.log"],
    capture_output=True,
    check=True,
    timeout=15
)
print(r.stdout.decode())

# 15: Requests per status code and per IP
# use CSV here to deal with delimeter, and even better if has header
print('15: Requests per status code and per IP')
with open('./lab3/access.log') as f:
    FIELDS = ["ip", "ident", "user", "ts", "tz", "request", "status", "bytes"]
    by_status, by_ip = Counter(), Counter()
    for row in csv.DictReader(f, delimiter=" ", quotechar='"', fieldnames=FIELDS):
        # None in Key and None in Values
        if None in row or None in row.values():
            print("Corrupted")
            continue
        else:
            by_ip[row["ip"]]+=1
            by_status[row["status"]]+=1
    {print(f'BY IP {k} Count: {v}') for k, v in by_ip.items()}
    {print(f'BY Status {k} Count: {v}') for k, v in by_status.items()}
    #     else:
    #         ip_col = row["ip"]
    #         dict_ip[ip_col] = dict_ip.get(ip_col, 0) + 1
    # {print(f'IP {k} Count: {v}') for k, v in dict_ip.items()}


# 15b. Requests per IP, sorted by count descending, ties broken by IP ascending (string order).
print('15b. Requests per IP, sorted by count descending, ties broken by IP ascending (string order).')
{print(*(f'By IP But sorted by count and tie break by ip string ascending - {k} Count: {v}' 
        for k, v in sorted(by_ip.items(), key=lambda kv: (kv[1], kv[0]) )
        ), sep="\n")
        }

# U can split sort in 2 many passes
# key doesnt have to be a lambda, can be a function, value can be a tuple, 
# and the sort will sort by the first element of the tuple, then the second, etc.
# number field can be negative to sort descending, or you can use reverse=True

for k, v in sorted(by_ip.items(), key=lambda kv: (kv[1], kv[0])):
    print(f'By IP But sorted by count and tie break by ip string ascending - {k} Count: {v}')

print('15b. using bash')
script_15 = r'''
    echo "By IP"
    awk 'NF==10 {print $1}' "$0" | sort | uniq -c | sort -k1,1nr -k2r;
    echo "BY Status"
    awk 'NF==10 {print $9}' "$0" | sort | uniq -c | sort -k1,1
'''
r = subprocess.run(
    ["bash", "-c", script_15, "lab3/access.log"],
    capture_output=True,
    check=True,
    timeout=15
)

print(r.stdout.decode())
# 16: Failed SSH logins per IP, plus usernames Dynamic fields, delimeter, 
# no header, hard to catch and deal with space, no quote, so use regex
print('16: Failed SSH logins per IP, plus usernames')
# \S+ means “a run of non-whitespace characters”. 
# \S is GNU-only. It works in GNU grep but may not on macOS. [^ ]+ works everywhere.
# For the IP it reads everything after from up to the next space,
# so it captures the whole address and stops at the gap before port
pattern_16 = r'Failed password for (.+) from (\S+)'
with open('./lab3/auth.log') as f:
    # by_user, by_ip = Counter(), Counter()
    # search return first
    # findall return list
    # m = re.search(pattern_16, line)
    m = re.findall(pattern_16, f.read())
    by_user = Counter(u for u, _ in m)
    by_ip   = Counter(i for _, i in m)
    {print(f'BY IP {k} Count: {v}') for k, v in by_ip.items()}
    {print(f'BY User {k} Count: {v}') for k, v in by_user.items()}


# -o flag - output matching only, 
# then print $NF output only ip because Ip is at the bottom
# use sed to remove and leave only certain part

script_16 = r'''
echo "By IP"
grep 'Failed password' "$1" | grep -oE 'for .+ from \S+' | awk '{print $NF}' | sort | uniq -c | sort -k1,1nr -k2,2;
echo "16b. Usernames targeted by failed logins, sorted by count descending."
grep 'Failed password' "$1" | grep -oE 'for .+ from \S+' | sed -E 's/^for (.+) from [^ ]+$/\1/' | sort | uniq -c | sort -k1,1nr;
# #   | grep -oE 'for .+ from [^ ]+' \
#   | awk 'print $NF' 
#   | sort | uniq -c | sort -k1,1nr -k2,2
#   | awk '{print $1, $2}'
'''

r =subprocess.run(["bash", "-c", script_16, "_", "lab3/auth.log"], check=True, capture_output=True, timeout=15)
print(r.stdout.decode())


# Summary
# 14. Technique: split each access-log line into fields; use awk as an alternative.
#     Note: whitespace splitting assumes a fixed field count and can misread quoted requests.
#     Changes: skip blank lines, report rows with an unexpected field count, and print timestamp/IP.
# 15. Technique: parse space-delimited rows with csv.DictReader and count IPs/statuses with Counter.
#     Note: quote-aware parsing keeps the request field together; malformed rows are skipped.
#     Changes: report counts grouped by IP and HTTP status.
# 15b. Technique: sort the IP counts by count and IP, in both Python and shell.
#      Note: current Python sorting is ascending by count; shell sorting is descending by count
#      but reverses the IP tie-break. Both differ from the stated descending-count/ascending-IP order.
#      Changes: print a sorted-by-count view of the per-IP totals.
# 16 (including 16b). Technique: capture usernames and source IPs with a regex, then count them;
#      use grep/sed/awk/sort as a shell alternative.
#      Note: the shell regex uses \S, which may not work with macOS's default grep -E.
#      Changes: report failed-login totals by source IP and username.
