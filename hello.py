arr = ["Hello", "World", "aaa"]


with open("output.txt", "w") as f:
    f.writelines("\n".join(arr))
    # f.write("\n")

with open('output.txt', "w") as f:
    f.write("\nAbc")
with open("output.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        print(line, end="")
with open("output.txt", "w"):
    pass
# print("haha")