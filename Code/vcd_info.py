import tkinter as tk
from tkinter import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilename
# import wave
from itertools import islice

f = open("../map9v3_tb.vcd", "rt")
lines = f.readlines()
date = version = timescale = comment = ""

scopeList = []
type_signal = []
signal_abbreviation = []
# type_abbreviation = []
lineNumber = 0
dictionaryNum = -1
count = 0


def header_info():
    global date, version, timescale, comment
    if "$date" in string:
        date = lines[lineNumber].lstrip().rstrip()
    if "$version" in string:
        version = lines[lineNumber].lstrip().rstrip()
    if "$timescale" in string:
        timescale = lines[lineNumber].lstrip().rstrip()
    if "$comment" in string:
        comment = lines[lineNumber].lstrip().rstrip()


def new_scope(scope_line):
    scopeList.append(string[14:len(scope_line) - 6] + ": line " + str(lineNumber))


for line in lines:
    lineNumber += 1
    string = line.rstrip()
    header_info()
    if string[:6] == "$scope":
        new_scope(string)
        # type_abbreviation.append({})
        type_signal.append({})
        signal_abbreviation.append({})
        dictionaryNum += 1
        continue
    if string[:4] == "$var":
        if "wire" in string:
            count += 1
            type_signal[dictionaryNum]["wire " + str(count)] = string[14:-5]
            signal_abbreviation[dictionaryNum][string[14:-5]] = string[12]
            # type_abbreviation[dictionaryNum][string[5:11]] = string[12]
        elif "reg" in string:
            count += 1
            type_signal[dictionaryNum]["reg " + str(count)] = string[13:-5]
            signal_abbreviation[dictionaryNum][string[13:-5]] = string[11]
            # type_abbreviation[dictionaryNum][string[5:10]] = string[11]


print("Date = " + date)
print("Version = " + version)
print("Timescale = " + version)
print(scopeList)

# for i in type_signal:
#     print(i)

for i in signal_abbreviation:
    print(i)

