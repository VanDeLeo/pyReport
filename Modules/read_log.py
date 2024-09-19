# made by leo

# Title: pyReport
# Autor: leonardo.avalos.montes@continental-corporation.com
# Position: Test Maintenance Technician
# Location: Continental Periferico - Guadalajara
# Date: 06/09/2024

import os
import datetime
from datetime import time
from tkinter import messagebox
import sys

shift1 = ["060001","151000"]
shift2 = ["151001","220000"]
shift3 = ["220001","060000"]

def getLogPath(logFolder):
    logFolder = os.path.abspath(logFolder)

    try:
        logList = os.listdir(logFolder)
    except FileNotFoundError:
        messagebox.showerror("Error", ("No se pudo encontrar la carpeta "+ logFolder))
        sys.exit(0)

    for log in logList:
        if datetime.date.today().strftime('%d-%m-%Y') in log:
            logPath = os.path.join(logFolder,log)
            return logPath
    
    messagebox.showerror("Error", ("No se encontraron logs en la carpeta " + logFolder + " cambie la ruta desde el archivo de configuracion o genere un log valido"))
    return sys.exit(0)

def convertTime(hour):
    return time(int(hour[:2]), int(hour[2:4]), int(hour[4:]))

def isInRange(actualHour, shiftStart, shiftEnd):
    if shiftStart <= shiftEnd:
        return shiftStart <= actualHour <= shiftEnd
    else:
        return actualHour >= shiftStart or actualHour <= shiftEnd

def getShift(logPath):
    shift1Start, shift1End = convertTime(shift1[0]), convertTime(shift1[1])
    shift2Start, shift2End = convertTime(shift2[0]), convertTime(shift2[1])
    shift3Start, shift3End = convertTime(shift3[0]), convertTime(shift3[1])
    actualHour = datetime.datetime.now().time()

    if isInRange(actualHour, shift1Start, shift1End):
        return 1, shift1Start, shift1End
    elif isInRange(actualHour, shift2Start, shift2End):
        return 2, shift2Start, shift2End
    elif isInRange(actualHour, shift3Start, shift3End):
        return 3, shift3Start, shift3End
    else:
        return 0,0,0
    
    

def readAll(logFolder):
    try:
        logPath = getLogPath(logFolder)
        shift, shiftStart, shiftEnd = getShift(logPath)
        shiftTests = []
        
        with open(logPath, "r") as file:
            data = file.readlines()
            for test in data[1:]:
                actualTest = test.split(",")
                startHour = actualTest[3]
                startHour = time(int(startHour[:2]),int(startHour[2:4]),int(startHour[4:]))
                #print((actualTest[0]+" "+str(startHour) + str(shift)))
                if isInRange(startHour, shiftStart,shiftEnd):
                    shiftTests.append(test)
    except FileNotFoundError:
        messagebox.showerror("Error", ("No se pudo encontrar el archivo "+ logPath))
        exit(0)

    return shiftTests

def readFails(logFolder):
    logData = readAll(logFolder)
    fails = []
    for data in logData:
        if "FAIL" in data:
            fails.append(data)

    return fails

def lastUnit(logFolder):
    try:
        last_test = readAll(logFolder)[-1]
        columns = last_test.split(",")
        return columns
    except IndexError:
        messagebox.showerror("Error", "No hay tests para registrar durante el turno en el .log")
        sys.exit(0)
    

def calculateFPY(logFolder):
    total_tests = readAll(logFolder)
    serials_status = {}
    
    if len(total_tests) == 0:
        return 0

    for test in total_tests:
        columns = test.split(",")
        serial = columns[0]
        status = columns[2]
        
        # Only consider the first record of the serial
        if serial not in serials_status:
            serials_status[serial] = status

    # Len how many serials without fails appears in the log
    serials_without_fails = sum(1 for status in serials_status.values() if status == "PASS")
    
    # Quantity of unique serials
    total_serials = len(serials_status)
    
    # Calculate FPY
    fpy = (serials_without_fails / total_serials) * 100 if total_serials > 0 else 0

    return fpy
    
