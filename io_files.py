import os

with open("demo.txt", "r") as f:
    # data = f.write("I am New to Python. Python is easy to learn.")
    data = f.read()
    new_data = data.replace("Python", "JAVASCRIPT")

with open("demo.txt", "w") as f:
    f.write(new_data)
    print(new_data)

    # print("File Closed:", f.closed)
