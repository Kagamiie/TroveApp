from configparser import ConfigParser
import configparser

config = ConfigParser()

def createConfig():

    config["DEFAULT"] = {
        "size": "670,385",
        "pos": "300,300"
    }

    with open("settings.ini", "w") as f:
        config.write(f)

def writeConfig(size = None, pos = None):

    try:
        config.read("assets/settings.ini")
    except configparser.MissingSectionHeaderError:
        createConfig()

    if size:
        config.set("DEFAULT", "size", size)
    if pos:
        config.set("DEFAULT", "pos", pos)

    with open("settings.ini", "w") as f:
        config.write(f)

def readConfig():
    
    try:
        config.read("assets/settings.ini")
    except configparser.MissingSectionHeaderError:
        createConfig()

    if not config["DEFAULT"].get("size"):
        size = "670,385"
        writeConfig(size="670,385")
    else:
        size = config["DEFAULT"].get("size")

    if not config["DEFAULT"].get("pos"):
        pos = "300,300"
        writeConfig(pos="300,300")
    else:
        pos = config["DEFAULT"].get("pos")

    return {"size":[int(i) for i in size.split(",")], "pos":[int(i) for i in pos.split(",")]}