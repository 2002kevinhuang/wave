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
scope_index = -1
signal_change = {}
definition_end = 0
temp_time = 0
abbreviation_multibit = {}


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
    global scope_index
    # scopeList.append(string[14:len(scope_line) - 6] + ": line " + str(lineNumber))
    scope_index += 1
    scopeList.append(string[14:len(scope_line) - 6] + " " + str(scope_index))


for line in lines:
    lineNumber += 1
    string = line.rstrip()
    header_info()
    if "$scope" in string:
        new_scope(string)
        # type_abbreviation.append({})
        type_signal.append({})
        signal_abbreviation.append({})
        # abbreviation_multibit.append({})
        dictionaryNum += 1
        continue
    if "$var" in string:
        if "wire" in string:
            count += 1
            type_signal[dictionaryNum]["wire " + str(count)] = string[14:-5]
            signal_abbreviation[dictionaryNum][string[14:-5]] = string[12]
            if "[" in string:
                if string.split()[5][1] != "e":
                    abbreviation_multibit[string[12]] = int(string.split()[5][1])
                else:
                    abbreviation_multibit[string[11]] = 0
            else:
                abbreviation_multibit[string[12]] = 0
            # type_abbreviation[dictionaryNum][string[5:11]] = string[12]
        elif "reg" in string:
            count += 1
            type_signal[dictionaryNum]["reg " + str(count)] = string[12:-5]
            signal_abbreviation[dictionaryNum][string[12:-5]] = string[11]
            if "[" in string:
                if string.split()[5][1] != "e":
                    abbreviation_multibit[string[11]] = int(string.split()[5][1])
                else:
                    abbreviation_multibit[string[11]] = 0
            else:
                abbreviation_multibit[string[11]] = 0
            # type_abbreviation[dictionaryNum][string[5:10]] = string[11]
    if "$enddefinitions" in line:
        definition_end = lineNumber

for scope in signal_abbreviation:
    for x in scope.values():
        if abbreviation_multibit[x] <= 0:
            signal_change[x.lstrip()] = [[], []]
        else:
            for i in range(0, abbreviation_multibit[x]+1):
                signal_change[x.lstrip() + "[" + str(i) + "]"] = [[], []]
# print(signal_change)


for line in lines[definition_end:]:
    string = line.lstrip().rstrip()
    if string[0] == "#":
        temp_time = string[1:]
        continue
    for scope in signal_abbreviation:
        for abbreviation in scope.values():
            if abbreviation != " ":
                if abbreviation_multibit[abbreviation] <= 0:
                    if (str(abbreviation) in string) and (temp_time not in signal_change[abbreviation][0]):
                        if string[0].isnumeric():
                            signal_change[abbreviation][0].append(temp_time)
                            signal_change[abbreviation][1].append(string[0])
                else:
                    for i in range(0, abbreviation_multibit[abbreviation]+1):
                        # print(abbreviation + "[" + str(i) + "]")
                        if (str(abbreviation) in string) and (temp_time not in signal_change[abbreviation + "[" + str(i) + "]"][0]) \
                                and (i <= len(string.split()[0])-2):
                            signal_change[abbreviation + "[" + str(i) + "]"][0].append(temp_time)
                            # print(string.split()[0])
                            signal_change[abbreviation + "[" + str(i) + "]"][1].append(string.split()[0][i+1])
                            # print(signal_change[abbreviation + "[" + str(i) + "]"])
                            # print(string.split()[0][i])
                            # signal_change[abbreviation + "[" + str(i) + "]"][1].append(string.split()[0][i+1])
                    # else:
                    #     for i in range(0, abbreviation_multibit[dictionaryNum][string[12]]+2):
                    #         signal_change[abbreviation][0].append(temp_time)
                    #         signal_change[abbreviation][1].append(string[0])

# print(abbreviation_multibit)
print(signal_change)

'''
print(signal_change)
print("Date = " + date)
print("Version = " + version)
print("Timescale = " + version)
print(scopeList)
# for i in type_signal:
#     print(i)
for i in type_signal:
    print(i) '''
#
# for x in scopeList:
#     print(x[-1])
