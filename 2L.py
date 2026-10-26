import re

import subprocess

arr = ["Mock ABC", "ABC123", "Start L2", "A", "C", "B", "C", "1", "2", "3"]



with open("2output.txt", "w") as f:
    f.writelines("\n".join(arr))

try:
    with open("2output.txt") as f:
        lines = f.readlines()
        print(len(lines))
    with open("2output.txt") as f:
        content = f.read()
        print(len(content.split()))
    with open("2output.txt") as f:
        print(len(f.read()))
    print("Find keyword, case sensitive, whole word")
    keyword = "s"
    pattern = r'\b' + keyword + r'\b'
    with open("2output.txt") as f:
        content = f.read()
        print(content.count(keyword))
        print(content.lower().count(keyword.lower()))
        print(re.findall(pattern, content, re.IGNORECASE))
    n = 3 
    for line in lines[-n:]:
        print(line, end='')

    print("Print certain lines")
    target_line={1, 3, 5}
    with open("2output.txt") as f:
        #start =1 rather than 0
        # Early exit optimisation: If your target lines are all near the top of a very large file, 
        # you can add if line_num > max(target_lines): break to stop reading once the last target line has been reached.
        for num, line in enumerate(f, start=1):
            if num in target_line:
                print(line, end="")
    print("Letter frequency")
    dict = {}
    with open("2output.txt") as f:
        content = f.read().lower()
    for char in content:
        if char.isalpha():
            dict[char] = dict.get(char, 0) + 1
    for k, v in dict.items():
        print(f"Key {k} Value {v}")

    print("Longest word")

    longest = ''
    with open("2output.txt") as f:
        content = f.read().split()
        for word in content:
            if len(longest) < len(word):
                longest = word
    print(longest)
    print("Word frequency (Top N)")

    dictWord = {}
    with open("2output.txt") as f:
        content = f.read().split()
        for word in content:
            dictWord[word] = dictWord.get(word, 0) + 1
        for k, v in dictWord.items():
            print(f"Key {k} Value {v}")
        for k, v in sorted(dictWord.items(), key= lambda item: item[1], reverse=True):
            print(k, v)
    print("Search word and in line")
    search_word = "C"
    pattern_word = r'\b' + search_word + r'\b'
    with open("2output.txt") as f:
        for line_num, line in enumerate(f, start=1):
            if re.findall(pattern_word, line, re.IGNORECASE):
                print(line_num)

    print("Search using sub process cmd")

    # When dont need pipe, redirect, command chaining
    # r = subprocess.run(
    #     ["grep", "-n", "-w", search_word],
    #     capture_output=True,
    #     text=True,
    #     timeout=15
    # )

    r = subprocess.run(
        f'cat 2output.txt | grep -nw {search_word}',
        shell=True,
        capture_output=True,
        # text=True,
        timeout=15
    )
    # Or decode afterwards: r.stdout.decode().
    decoded_byte = r.stdout.decode()
    print(decoded_byte)
except FileNotFoundError as e:
    print("File not found", e)