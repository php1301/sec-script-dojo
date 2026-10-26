import re 
import subprocess
import csv

arr = ["ex 3", "Mock 3ABC", "XYZ123", "Start L2", "A", "C", "B", "C", "1", "2", "3", "  Hello World  ", " PYPYTHONTON   "]


output_file = "3output.txt"
organized_file = "3organized.txt"
with open(output_file, "w") as f:
    f.writelines("\n".join(arr))

with open(output_file) as f:
    print(f.readlines())

# Default to for line in infile.
#  Use readlines() only when you need the whole file in memory as a list.

print("\n Strip whitespace and swap case, saving to a new file, ouble With")

with open(output_file) as infile, open(organized_file, "w") as outfile:
    for line in infile:
        outfile.write(line.strip().swapcase() + "\n")

old_word = "Java"
new_word = "Python"
with open("3replace.txt", "w") as f:
    f.write("I love Java. Java is great.")

with open("3replace.txt") as f:
    content = f.read()

replaced_content = content.replace(old_word, new_word)

with open("3replace.txt", "w") as f:
    f.write(replaced_content)

with open(organized_file) as f:
    print(f.readlines())


def isemail(email):
    # pattern = r'[a-zA-Z0-9]+@[a-z]+(\.[a-z]+)+'

    # ?: makes the group non-capturing
    # A normal ( ) does two jobs: it groups, and it saves what it matched. 
    # findall then returns only the saved part.
    pattern = r'[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-z]+(?:\.[a-z]+)+'
    return re.findall(pattern, email)

print("13a. Print every email in data.txt, in order of appearance.")
with open("./lab3/data.txt") as f:
    content = f.readlines()
    email_list = set()
    for line in content:
        emails = isemail(line)
        if emails:
            # add puts one element into a set. 
            # update puts in every element of an iterable.
            email_list.update(emails)

    print(email_list)
print("13b. Same, but unique and sorted.")
r = subprocess.run(
    f'cat lab3/data.txt | grep -oE "[a-zA-Z0-9]+(\.[a-zA-Z]+)*@[a-z]+(\.[a-z]+)+ | sort | uniq" ',
    capture_output=True,
    timeout=15,
    shell=True
)
print(r.stdout.decode())
print("13c. From users.csv, print the name of everyone in dept sec, skipping the header.")
with open('./lab3/users.csv') as f:
    header = f.readline().strip().split(',')
    # enumerate walks through a list and hands you (position, item) pairs, 
    # so you get the index without managing a counter yourself.
    idx = {name: i for i, name in enumerate(header)}

    content = f.readlines()
    # print(content)
    # OR
    # for line in f
    for line in content:
        if not line.strip():
            continue
        cols = line.strip().split(',')
        if cols[idx['dept']] == "sec": # to find the column number of dept
            print(cols[idx['name']])

print("13c. use lib csv")
with open('./lab3/users.csv') as f:
    for row in csv.DictReader(f):
        if row["dept"] == "sec":
            print(row["name"])
print("13c. use bash")

# $0 is unquoted, so a path with spaces splits into two arguments
script_13c = r'''
    awk -F, '{ if (NR>1 && $3 == "sec" ) print $2}' "$0"
'''
r = subprocess.run(
    ["bash", "-c", script_13c, "lab3/users.csv"],
    capture_output=True,
    timeout=15
)
print(r.stdout.decode(), end='')

print("13d. Total salary, and salary per dept.")

with open('./lab3/users.csv') as f:
    header = f.readline().strip().split(',')
    idx = {name: i for i, name in enumerate(header)}
    total_salary = 0
    dept_salary = {}
    for line in f:
        if not line.strip():
            continue
        cols = line.strip().split(',')
        dept_col = cols[idx['dept']]
        salary_col = int(cols[idx['salary']])
        dept_salary[dept_col] = dept_salary.get(dept_col, 0) + salary_col
        total_salary = total_salary + salary_col
    print(f"Total salary {total_salary}")
    {print(f"Dept {k}: {v}") for k, v in dept_salary.items()}

print("13d. use lib csv")
with open('./lab3/users.csv') as f:
    csv_total_salary = 0
    csv_dept_salary = {}
    for row in csv.DictReader(f):
        salary_data = int(row["salary"])
        csv_dept_salary[row["dept"]] = csv_dept_salary.get(row["dept"], 0) + salary_data
        csv_total_salary = csv_total_salary + salary_data
    print(f'Total in CSV {csv_total_salary}')
    {print(f'In CSV - Dept {k}: {v}') for k, v in csv_dept_salary.items()}
print("13d. use bash")

# awk -F, '
# BEGIN { total = 0 }
# NR>1  { d[$3] += $4; total += $4 }
# END   { print total; for (k in d) print k, d[k] }
# ' lab3/users.csv

script_13d = r'''
    awk -F, '
    BEGIN {total = 0}
    NR>1 {
    total+=$4;
    d[$3]+=$4
    }
    END {
        print total;
        for (k in d) print k, d[k]
    }
    ' "$0"
'''
r = subprocess.run(
    ["bash", "-c", script_13d, "lab3/users.csv"],
    timeout=15,
    capture_output=True,
    # text=True,
    check=True
)

print(r.stdout.decode())


