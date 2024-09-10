import os
import datetime
from tkinter import messagebox

def getLogPath(logFolder):
    logFolder = os.path.abspath(logFolder)

    logList = os.listdir(logFolder)

    for log in logList:
        if datetime.date.today().strftime('%d-%m-%Y') in log:
            logPath = os.path.join(logFolder,log)
            break
    return logPath

def readAll(logFolder):
    try:
        logPath = getLogPath(logFolder)
        with open(logPath, "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        messagebox.showerror("Error", ("No se pudo encontrar el archivo "+ logPath))
        exit(0)

    return data[1:]

def readFails(logFolder):
    logData = readAll(logFolder)
    fails = []
    for data in logData:
        if "FAIL" in data:
            fails.append(data)

    return fails

def lastUnit(logFolder):
    last_test = readAll(logFolder)[-1]
    columns = last_test.split(",")

    return columns

# def calculateFPY(logFolder):
#     total_tests = readAll(logFolder)
#     serials_processed = set()
#     serials_without_fails = 0

#     if len(total_tests) == 0:
#         return 0

#     for test in total_tests:
#         columns = test.split(",")
#         serial = columns[0]
#         status = columns[2]

#         if serial not in serials_processed:
#             serials_processed.add(serial)
#             if status == "PASS":
#                 serials_without_fails+=1
    
#     fpy = (serials_without_fails / len(total_tests)) * 100

#     return fpy
def calculateFPY(logFolder):
    total_tests = readAll(logFolder)
    serials_status = {}
    
    if len(total_tests) == 0:
        return 0

    for test in total_tests:
        columns = test.split(",")
        serial = columns[0]
        status = columns[2]
        
        # Solo considerar el primer registro del serial
        if serial not in serials_status:
            serials_status[serial] = status

    # Contar cuántos seriales no tienen fallos en su primera aparición
    serials_without_fails = sum(1 for status in serials_status.values() if status == "PASS")
    
    # Número total de seriales únicos procesados
    total_serials = len(serials_status)
    
    # Calcular FPY
    fpy = (serials_without_fails / total_serials) * 100 if total_serials > 0 else 0

    return fpy
    
