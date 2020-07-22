import matplotlib.pyplot as plt
import numpy as np


input_amp = [1,0,1,0,1,0,1,0,1,0]
plt.style.use('dark_background')
plt.plot(input_amp, color="#39ff14",linewidth=.5,drawstyle='steps-post')
plt.title("Waveform")
plt.ylabel('Amplitude')
plt.yticks([0,1])
plt.xlabel("Time (Seconds)")
plt.xticks([i for i in range(10)])
plt.show()
