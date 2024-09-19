# made by leo

# Title: pyReport
# Autor: leonardo.avalos.montes@continental-corporation.com
# Position: Test Maintenance Technician
# Location: Continental Periferico - Guadalajara
# Date: 06/09/2024

import configparser
import os.path as path
from Modules.tools import resource_path

configPath = path.abspath(resource_path("./Config/config.ini"))
config = configparser.ConfigParser()

def all_config():
    config.read(configPath)

    projectName = config["DATA"]["ProjectName"]
    stationName = config["DATA"]["StationName"]
    sapID = config["DATA"]["SAPID"]
    updateRate = config["SETTINGS"]["UpdateRate"]
    logFolder = config["PATHS"]["LogFolder"]

    return(projectName, stationName, sapID, updateRate, logFolder)

def save_all(projectName, stationName, sapID, updateRate, logFolder):

    config["DATA"]["ProjectName"] = projectName
    config["DATA"]["StationName"] = stationName
    config["DATA"]["SAPID"] = sapID

    config["SETTINGS"]["UpdateRate"] = updateRate

    config["PATHS"]["LogFolder"] = logFolder

    with open(configPath, "w") as configFile:
        config.write(configFile)
        return True
    
    return False
