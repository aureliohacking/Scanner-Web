import os

path = str(os.getcwd())

try:
    os.system("git clone https://github.com/hahwul/XSpear")
    os.chdir(path + "/XSpear/")
    os.system("gem install XSpear-1.4.1.gem")
except Exception as e:
    print('Error: ' + str(e))
a = input('Presiona enter para continuar')