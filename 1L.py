import os 

if os.path.exists('output.txt'):
    print('File exists')
else:
    print("No")

try:
    with open('output.txt') as f:
        content = f.readlines()
        print(content)
except FileNotFoundError as e:
    print("Not exists try catch")