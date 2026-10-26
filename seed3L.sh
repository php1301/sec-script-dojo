mkdir -p ./lab3 && cd ./lab3

cat > data.txt <<'EOF'
Contact alice@example.com or bob.smith@corp.co.uk for access.
No email on this line.
Reach support: help+vpn@company.io, cc: carol_99@test-site.org
Invalid: @nouser.com, user@, plain.text
Duplicate: alice@example.com again
EOF

cat > users.csv <<'EOF'
id,name,dept,salary
1,alice,eng,5000
2,bob,sec,4500
3,carol,eng,5200
4,dave,ops,4000
5,erin,sec,4800
EOF

cat > access.log <<'EOF'
203.0.113.5 - - [10/Oct/2026:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
198.51.100.7 - - [10/Oct/2026:13:55:40 +0000] "GET /login HTTP/1.1" 200 1500
203.0.113.5 - - [10/Oct/2026:13:56:01 +0000] "POST /login HTTP/1.1" 302 0
192.0.2.9 - - [10/Oct/2026:13:56:10 +0000] "GET /admin HTTP/1.1" 404 512
203.0.113.5 - - [10/Oct/2026:13:57:22 +0000] "GET /search?q=test HTTP/1.1" 200 900
THIS LINE IS CORRUPTED
198.51.100.7 - - [10/Oct/2026:13:58:00 +0000] "GET /index.html HTTP/1.1" 200 2326
192.0.2.9 - - [10/Oct/2026:13:58:30 +0000] "GET /admin HTTP/1.1" 404 512
203.0.113.5 - - [10/Oct/2026:13:59:00 +0000] "GET /about HTTP/1.1" 200 800
10.0.0.8 - - [10/Oct/2026:14:01:15 +0000] "GET /api/v1/users HTTP/1.1" 500 128
EOF

cat > auth.log <<'EOF'
Oct 22 09:00:01 srv sshd[101]: Failed password for root from 45.9.1.1 port 4001 ssh2
Oct 22 09:00:05 srv sshd[102]: Failed password for admin from 45.9.1.1 port 4002 ssh2
Oct 22 09:00:09 srv sshd[103]: Accepted password for alice from 10.0.0.5 port 5001 ssh2
Oct 22 09:01:12 srv sshd[104]: Failed password for root from 91.2.3.4 port 4003 ssh2
Oct 22 09:01:20 srv sshd[105]: Failed password for invalid user test from 45.9.1.1 port 4004 ssh2
Oct 22 09:02:00 srv sshd[106]: Accepted password for bob from 10.0.0.6 port 5002 ssh2
Oct 22 09:02:30 srv sshd[107]: Failed password for root from 91.2.3.4 port 4005 ssh2
Oct 22 09:03:00 srv sshd[108]: Failed password for root from 45.9.1.1 port 4006 ssh2
EOF