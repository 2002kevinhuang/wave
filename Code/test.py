import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = Tk()
'''
figure = plt.Figure(figsize=(5, 4), dpi=120)
plot = figure.add_subplot(1, 1, 1, yticks=[0, 1], facecolor='black', title="Waveform", ylabel='Amplitude',xlabel="Time (Seconds)")
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack(side=RIGHT)
y = [1,1,0,0,1,0,1]
x = [1,2,3,4,5,6,7]
plot.plot(x,y,color="#39ff14", linewidth=.5, drawstyle='steps-post')'''

y = [1,1,0,0,1,0,1]
x = [1,2,3,4,5,6,7]

y1 = [1,1,0,0,1,0,1]
x1 = [1,8,9,10,11,12,13]

fig, axs = plt.subplots(2, sharex=True)
axs[0].plot(x, y,color="#39ff14", linewidth=.5, drawstyle='steps-post')
axs[0].set_facecolor('black')
axs[0].set_yticks([0,1])
axs[1].plot(x1, y1,color="#39ff14", linewidth=.5, drawstyle='steps-post')
axs[1].set_facecolor('black')
axs[1].set_yticks([0,1]))


canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack()
