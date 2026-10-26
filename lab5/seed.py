# L5 seed generator. Usage: mkdir L5 && cd L5 && python3 ../gen_l5_seed.py
# Deterministic (random.seed(2026)), writes the 8 data files into the current directory.
import random, datetime as dt, urllib.parse as up, csv
import os
random.seed(2026)
base = dt.datetime(2026,10,25,8,0,0)
def ts(s): return (base+dt.timedelta(seconds=s))
os.chdir('./lab5')

# ---------- E24 access.log (SQLi, URL-encoded) ----------
benign = ["/index.html","/login","/api/v1/users?id=42","/search?q=laptops","/static/app.js","/api/v1/orders?status=open","/products?category=books&page=2","/search?q=select+a+gift","/about","/contact"]
sqli = ["/products?id=1' OR '1'='1","/search?q=' UNION SELECT username,password FROM users--","/api/v1/users?id=1; DROP TABLE users;--","/login?user=admin'--","/item?id=1 AND SLEEP(5)","/search?q=1' AND 1=CONVERT(int,@@version)--","/api/v1/users?id=5 OR 1=1"]
ips = ["203.0.113.%d"%i for i in range(10,30)]
lines=[]; sqli_idx=[]
t=0
for i in range(120):
    t+=random.randint(1,9)
    ip=random.choice(ips)
    if i in (7,19,33,48,61,77,90,104):
        u=sqli[len(sqli_idx)%len(sqli)]
        # encode query part; leave first two with partial encoding
        path,_,q=u.partition("?")
        u=path+"?"+up.quote(q,safe="=&") if i%2==0 else path+"?"+up.quote(q,safe="=&'")
        sqli_idx.append(i); ip="198.51.100.77" if i%3==0 else ip
    else:
        u=random.choice(benign)
    status=random.choice([200,200,200,302,404,500])
    lines.append('%s - - [%s] "GET %s HTTP/1.1" %d %d "-" "Mozilla/5.0"'%(ip,ts(t).strftime("%d/%b/%Y:%H:%M:%S +0000"),u.replace(" ","%20") if "%" not in u else u,status,random.randint(200,9000)))
open("E24_access.log","w").write("\n".join(lines)+"\n")

# ---------- E25 + E31 netflow.csv ----------
rows=[]
def flow(t,src,dst,port,proto,b,p): rows.append((ts(t).strftime("%Y-%m-%d %H:%M:%S"),src,dst,port,proto,b,p))
internal=["10.0.1.%d"%i for i in range(10,40)]
servers=["10.0.9.5","10.0.9.6","10.0.9.7"]
for _ in range(700):
    s=random.choice(internal); d=random.choice(servers); pt=random.choice([80,443,443,443,53,22])
    flow(random.randint(0,3500),s,d,pt,"tcp" if pt!=53 else "udp",random.randint(300,20000),random.randint(2,40))
# big-bytes, few flows: backup host
for _ in range(12): flow(random.randint(0,3500),"10.0.1.99","10.0.9.6",443,"tcp",random.randint(80_000_000,120_000_000),random.randint(50000,90000))
# vertical scanner: one host, 150 ports, tiny
for i,pt in enumerate(range(1,151)): flow(1200+i//3,"192.0.2.66","10.0.9.5",pt,"tcp",60,1)
# horizontal sweeper: 40 hosts, port 445
for i in range(1,41): flow(2000+i,"192.0.2.88","10.0.2.%d"%i,445,"tcp",60,1)
# noisy but legit: many flows to ONE dst/port (not a scanner)
for i in range(180): flow(100+i*15,"10.0.1.20","10.0.9.7",443,"tcp",random.randint(500,1500),3)
random.shuffle(rows); rows.sort(key=lambda r:r[0])
with open("E25_E31_netflow.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["timestamp","src_ip","dst_ip","dst_port","proto","bytes","packets"]); w.writerows(rows)

# ---------- E26 app_events.log (per-minute) ----------
ev=[]
levels=["INFO","INFO","INFO","WARN","ERROR"]
minute_counts={0:5,1:8,2:3,3:0,4:0,5:12,6:4,7:30,8:6,9:1}   # minutes 3,4 intentionally empty
for m,c in minute_counts.items():
    for _ in range(c):
        ev.append((m*60+random.randint(0,59),random.choice(levels)))
ev.sort()
open("E26_app_events.log","w").write("".join("%s %s event_%03d\n"%(ts(s).strftime("%Y-%m-%dT%H:%M:%SZ"),l,i) for i,(s,l) in enumerate(ev)))

# ---------- E27 + E30 auth.log ----------
au=[]
def a(t,kind,user,ip,pid=None):
    pid=pid or random.randint(1000,9999)
    if kind=="F": msg="Failed password for %s%s from %s port %d ssh2"%("invalid user " if user in("admin","test","oracle") else "",user,ip,random.randint(30000,60000))
    else: msg="Accepted password for %s from %s port %d ssh2"%(user,ip,random.randint(30000,60000))
    au.append((t,"%s sshd[%d]: %s"%(ts(t).strftime("%Y-%m-%d %H:%M:%S"),pid,msg)))
# normal users
for u,ip in [("alice","10.0.1.11"),("bob","10.0.1.12"),("carol","10.0.1.13"),("dave","10.0.1.14")]:
    for k in range(3): a(random.randint(0,3000),"S",u,ip)
a(500,"F","alice","10.0.1.11"); a(520,"S","alice","10.0.1.11")          # 1 typo then ok: NOT suspicious
a(900,"F","bob","10.0.1.12"); a(910,"F","bob","10.0.1.12"); a(930,"S","bob","10.0.1.12")  # 2 fails then ok: NOT
# brute force from 203.0.113.50 on root/admin/test: 7 fails, never succeeds
for i,u in enumerate(["root","admin","test","root","admin","oracle","root"]): a(1000+i*4,"F",u,"203.0.113.50")
# brute force that SUCCEEDS: 5 fails on carol then ok from 198.51.100.9
for i in range(5): a(1500+i*6,"F","carol","198.51.100.9")
a(1540,"S","carol","198.51.100.9")
# exactly 3 fails (edge) then ok on dave from 192.0.2.200
for i in range(3): a(2000+i*5,"F","dave","192.0.2.200")
a(2030,"S","dave","192.0.2.200")
# exactly 2 fails from one IP (below threshold)
a(2200,"F","root","203.0.113.60"); a(2210,"F","root","203.0.113.60")
# success BEFORE failures (order trap): erin ok, then 4 fails
a(2500,"S","erin","10.0.1.15")
for i in range(4): a(2510+i*5,"F","erin","203.0.113.70")
# slow brute force: 3 fails spread over 40 min from 203.0.113.80
for i in range(3): a(300+i*1200,"F","admin","203.0.113.80")
au.sort()
open("E27_E30_auth.log","w").write("\n".join(l for _,l in au)+"\n")

# ---------- E28 two logs: firewall.log + proxy.log ----------
fw=[];px=[]
for _ in range(40):
    fw.append((random.randint(0,3000),random.choice(["10.0.1.%d"%i for i in range(10,16)]),random.choice([23,3389,445,8080]),"DENY"))
for _ in range(60):
    px.append((random.randint(0,3000),random.choice(["10.0.1.%d"%i for i in range(10,18)]),random.choice(["news.example.com","cdn.example.net","mail.example.org","files.example.io"])))
fw.sort(); px.sort()
open("E28_firewall.log","w").write("".join("%s src=%s dport=%d action=%s\n"%(ts(t).strftime("%Y-%m-%d %H:%M:%S"),s,p,ac) for t,s,p,ac in fw))
open("E28_proxy.log","w").write("".join("%s client=%s host=%s\n"%(ts(t).strftime("%Y-%m-%d %H:%M:%S"),s,h) for t,s,h in px))

# ---------- E29 alerts.csv + hosts.csv ----------
hosts=[("10.0.1.%d"%i,"ws-%02d.corp.local"%i) for i in range(10,20)]+[("10.0.9.5","db-01.corp.local"),("10.0.9.6","backup-01.corp.local")]
open("E29_hosts.csv","w").write("ip,hostname\n"+"".join("%s,%s\n"%h for h in hosts))
rules=["Brute force","Port scan","Malware beacon","Impossible travel"]
al=["alert_id,timestamp,src_ip,rule"]
for i in range(1,21):
    ip=random.choice(["10.0.1.%d"%random.randint(10,24)]+["10.0.9.5","192.0.2.66","203.0.113.50"])
    al.append("A%03d,%s,%s,%s"%(i,ts(random.randint(0,3000)).strftime("%Y-%m-%d %H:%M:%S"),ip,random.choice(rules)))
open("E29_alerts.csv","w").write("\n".join(al)+"\n")