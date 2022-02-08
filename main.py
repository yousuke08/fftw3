from collections import defaultdict
import os,shutil,locale,json
from typing import DefaultDict, Text
import PySimpleGUI as sg
from datetime import datetime as dt

layout = [[sg.Text('My one-shot window.')],      
                 [sg.InputText()],      
                 [sg.Submit(), sg.Cancel()]]      

window = sg.Window('Window Title', layout)    

event, values = window.read()    
window.close()