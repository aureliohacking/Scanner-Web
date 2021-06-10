import sys

try:
    file_path = sys.argv[1]
    with open(file_path, "r") as f:
        r = str(f.read())
        print(r)
except Exception as e:
    print('Error' + str(e))

a = input('Presiona enter para continuar')