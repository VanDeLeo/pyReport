# made by leo

# Title: pyReport
# Autor: leonardo.avalos.montes@continental-corporation.com
# Position: Test Maintenance Technician
# Location: Continental Periferico - Guadalajara
# Date: 06/09/2024

from sys import argv
import os.path as path
import datetime

def create_file(fileFullPath):
    with open(fileFullPath, 'w') as file:
        file.write("[SERIAL - PARTNUMBER - TEST STATUS - TEST START - TEST END - FAIL MODE - TEST RESULT - TEST LIMITS]")
        file.close()
    append_data(fileFullPath)

def append_data(fileFullPath):
    with open(fileFullPath, "a") as file:
        file.write("\n" + serial + "," + partNumber + "," + testStatus + "," + testStart + "," + testEnd + "," + failMode + "," + testResult + "," + testLimits)
        file.close()

def main():
    fileFullPath = path.join(filePath,fileName+"_"+datetime.date.today().strftime('%d-%m-%Y')+".log")
    print(fileFullPath)
    if path.exists(fileFullPath) != True:
        create_file(fileFullPath)
    else:
        append_data(fileFullPath)
        

if __name__ == "__main__":
    filePath = argv[1]
    fileName = argv[2]
    serial = argv[3]
    partNumber = argv[4]
    testStatus = argv[5]
    testStart = argv[6]
    testEnd = argv[7]
    failMode = argv[8]
    testResult = argv[9]
    testLimits = argv[10]

    main()