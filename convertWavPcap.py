import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "rb") as binary_file:
        # Read the whole file at once
        data = (binary_file.read())
        # print(data.replace('\\', ' '))
        print(data.hex())


    
