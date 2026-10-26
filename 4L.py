from pathlib import Path
import os
import string

LAB4_DIR = Path(__file__).resolve().parent / "lab4"
LAB4_DIR.mkdir(parents=True, exist_ok=True)
# That changes the process’s working directory, so relative paths—such as "output17.txt"—resolve inside lab4.
# Absolute paths are unaffected.
os.chdir(LAB4_DIR)

# Mock array for the file-related exercises.
mock_files = [Path(name) for name in ("report.txt", "data.csv", "notes.log")]
mock_contents = [
    "Quarterly report\nRevenue increased by 8 percent.\nExpenses remained steady.\n",
    "id,name,amount\n1,Ada,125.50\n2,Grace,200.00\n",
    "INFO Service started\nERROR Connection timed out\nINFO Retry scheduled\nERROR Retry limit reached\n",
]
for file_path, content in zip(mock_files, mock_contents):
    if not file_path.exists():
        file_path.write_text(content, encoding="utf-8")

print("Mock files:", mock_files)


# E17	File size in KB, and list files only (no dirs) into a file	PN 23, 30
print("E17: File size in KB, and list files only (no dirs) into a file")
output_path_17 = 'output17.txt'
with open(output_path_17, "w") as f:
    res_size = str(os.path.getsize(mock_files[0]))
    print(f'File size: {res_size} ')
    file_in_dir_res = os.listdir('.')
    f.writelines('\n'.join([res_size, *file_in_dir_res]))

# E18	Rename multiple files with a prefix, and delete safely	PN 25-27
print("E18: Rename multiple files with a prefix, and delete safely")
try:
    output_path_18 = 'output18.txt'
    os.rename(output_path_17, output_path_18)
    # mutiple files rename with a prefix
    prefix = '2026_'
    for filename in os.listdir(os.curdir):
        # old_path = os.path.join(os.curdir)
        if filename.endswith('.abc'):
        # old_path = os.path.join(directory, filename)
        # new_path = os.path.join(directory, prefix + filename)
        # os.rename(old_path, new_path)
            os.rename(filename, prefix+filename)
except Exception as e:
    print(e)
    
# E19	Merge two files, and reverse line order	PN 28, 29
print("E19: Merge two files, and reverse line order")

with open('merged.txt', "w") as f:
    list_merge = ["output17.txtL4", "2026_report.txt"]
    for filename in list_merge:
        with open(filename) as fname:
            f.write(fname.read())
            f.write("\n")

with open('merged.txt') as infile, open('merged_reverse.txt', 'w') as outfile:
    reversed_line = infile.readlines()[::-1]
    arr = [line for line in reversed_line if line.split()]
    print(len(arr))
    outfile.writelines(arr)
# E20	Binary copy in chunks, verified with a checksum	PN 24, 31
# This exercise introduces binary file I/O, which is essential for handling non-text files. 
# It reinforces the read-then-write pattern while highlighting the difference between text mode and binary mode in Python.
# so that the program works correctly for all file types including images, PDFs, and executables.

print("E20: Binary copy in chunks, verified with a checksum")
# open("source.txt", "rb"): Opens the source file in binary read mode. The b flag tells Python to treat the file as raw bytes rather than decoded text, 
# preventing any newline or encoding translations.
# open("destination.txt", "wb"): Opens (or creates) the destination file in binary write mode. 
# If the file already exists, its content is overwritten.
# src.read(): Reads the entire file as a bytes object. This works for any file type since no decoding is applied.
# dst.write(data): Writes the raw bytes directly to the destination file, producing an exact byte-for-byte copy of the original.
# Note: For very large files, reading in chunks (e.g., src.read(4096) in a loop) is more memory-efficient 
# than reading everything at once.
with open("merged_copy.txt", "wb") as outfile, open('merged_reverse.txt', "rb") as infile:
    src = infile.read()
    outfile.write(src)

# E21	Unique sorted words	PN 32 - translate, maketrans, set, sort
# First parameter (""): Empty string (no characters to replace).

# Second parameter (""): Empty string (no replacement characters).

# Third paramete: Characters to delete (all punctuation). The translate() method removes these characters from the string.

# The .translate() method takes the translation table created by maketrans() 

# and scans through your text string character by character:

# Lookup: For every single character in your string
# Python checks if it exists (a character from x) in the translation table then replace.
#Speed: Because Python builds an internal mapping table,
# this operation happens in a single, highly optimized pass,
# making it much faster than chaining multiple .replace() methods.
print("E21: Unique sorted words")
with open('paragraph.txt') as f:
    content_21 = f.read().lower()
    words = content_21.translate(content_21.maketrans("", "", string.punctuation)).split()
    unique_words = set(sorted(words))

    [print(w, sep="\n") for w in unique_words]
# E22	Filter ERROR lines and save them	PN 33

# Use .strip() when printing to remove trailing newline characters from each matching line.
print("E22: Filter ERROR lines and save them")
keyword = "ERROR"
with open('notes.log') as f:
    for line in f:
        if keyword in line:
            print(line.strip())
# E23	Split a file into 10-line parts	PN 34
print("E23: Split a file into 10-line parts")

with open('2026_output18.txt') as f:
    lines = [line for line in f.readlines() if line.split()]

total_lines = len(lines)

chunk = 6
count = 0
start = 0
for i in range(0, total_lines, chunk):
    count+=1
    with open(f'chunk_{count}_2026_output18.txt', "w") as f:

        extracted_lines = lines[start:start+chunk]
        start += chunk
        f.writelines(extracted_lines)