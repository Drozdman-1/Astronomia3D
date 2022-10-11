from func_tools import *
import json
import subprocess



data ={'n': 'Planets', 'ln': '', 'd': ['1769', '8', '15'], 't': ['11', '00', '00'], 'd_utc': '15-08-1769', 't_utc': '10:51:00', 'z': '+0200', 'tz': 'Europe/Paris', 'tn': 'Ajaccio', 'cy': 'France', 'lat': '41.948', 'lon': '8.758', 'acc': 1, 'timestamp': -6323317740.0, 'trueNode': True, 'obliquity': 23.438}

data["trueNode"]=True
str_=str(data)
print('',str_); 
script_path=r"astronomia3D.py"
subprocess.call(["python.exe", script_path, str_, "standalone"])





