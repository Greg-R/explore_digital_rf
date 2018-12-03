#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 12:55:51 2018

Read a GRC file sink, FFT and plot.

@author: raven
"""

import numpy as np
from scipy.fftpack import fft
from scipy.signal import blackman, blackmanharris
from scipy.fftpack import fftshift, fftfreq
from MakePdfGraph import MakePdfGraph

#with np.fromfile('/home/raven/file_sink_data', dtype=np.complex64) as f:
#    for data in f:
#        print(data)

num_samples = 1024

raw_data = np.fromfile('/home/raven/file_sink_data', dtype=np.complex64)

start = 50000
stop = start + 1024

data = raw_data[start:stop]

print(raw_data[10000:10010])

t = np.arange(0, num_samples, 1)

w = blackman(num_samples)
#  Now compute the FFT and display.
y_average = np.zeros(1024)
y100_average = 0

#  Use a loop to video average:
for increment in range(10):
    start = 10000 + 1024 * increment
    stop = start + 1024
    y = -np.absolute(20.0*np.log10(fft(raw_data[start:stop] * w)/1024.0))
    y_plot = fftshift(y)
    y100_average = y100_average + y_plot[100]    
    y_average = y_average + y_plot

graph2 = MakePdfGraph(t, y_average/10)
graph2.display()



