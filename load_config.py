import os, json

def loadConfig():
    workpath = os.path.abspath(os.path.join(os.getcwd(), ""))
    config_path = workpath+'/config.json'
    f = open(config_path,'r', encoding='UTF-8')
    configs = json.load(f)
    return configs