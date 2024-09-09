import configparser
import os.path as path

configPath = path.abspath("./Config/config.ini")
config = configparser.ConfigParser()

def all_config():
    config.read(configPath)

    projectName = config["DATA"]["ProjectName"]
    stationName = config["DATA"]["StationName"]
    updateRate = config["SETTINGS"]["UpdateRate"]
    logFolder = config["PATHS"]["LogFolder"]

    return(projectName, stationName, updateRate, logFolder)