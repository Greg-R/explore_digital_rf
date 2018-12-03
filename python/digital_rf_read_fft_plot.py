#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 07:02:55 2018

Process HDF5 data and plot RF Spectrum.

@author: raven
"""

import digital_rf as drf
import numpy as np
from scipy.fftpack import fft
from scipy.signal import blackman
from scipy.fftpack import fftshift, fftfreq
from MakePdfGraph import MakePdfGraph

#  Path to HDF5 data:
hdf5_data = '/home/raven/digital_rf_data'

#  Read the Digital RF data:
try:
    do = drf.DigitalRFReader(hdf5_data)
except ValueError:
    print('HDF5 data is missing or corrupted')

#  Get the list of channel names and print (only 1 in this example):
channels = do.get_channels()
print(f'\nA list of the channels in the data: {str(channels)}\n')

#  Get the "bounds" in epoch time times sample rate:
s, e = do.get_bounds('fm_receiver')
print(f'The bounds are {s} to {e}.\n')

#  Use the same number of samples as GRC QT GUI Sink.
num_samples = 1024

#  The data is stored in 1 second chunks at 10MHz sample rate.
#  Skip forward 2.5 seconds to avoid start-up transients.
#  Read at least enough for average 10 1024 sample frames.
raw_data = do.read_vector(s + 25000000, num_samples * 10000, 'fm_receiver')

#  The data is a vector of complex numbers:
print("A sample of the raw data, which is a numpy array:")
print(raw_data[10000:10010])

fm_receiver_folder = hdf5_data + '/fm_receiver/metadata'

#  Read the meta-data:
try:
    dmr = drf.DigitalMetadataReader(fm_receiver_folder)
except IOError:
    print('Did not find metadata folder.')
    raise

#  Get the sample rate and print:
sps = dmr.get_samples_per_second()
print(f'\nSamples per second from metadata: {sps}')

#  Need an FFT with 1024 samples to match the GNU Radio QT sink display.
#  Compute the FFT and display.

#  Set up the x axis:
xf = fftfreq(num_samples, 1/sps)
center_frequency = 101.1e6
xf = fftshift(xf) + center_frequency

#  Blackman windowing.
w = blackman(num_samples)

#  Now compute the FFT and display.
y_average = np.zeros(1024)

#  Use a loop to video average:
for increment in range(10):
    start = 50000 + 1024 * increment
    stop = start + 1024
    y = -np.absolute(20.0*np.log10(fft(raw_data[start:stop] * w)/1024.0))
    y_plot = fftshift(y)
    y_average = y_average + y_plot

y_average = y_average/10

spectrumPlot = MakePdfGraph(xf, y_average)
spectrumPlot.display()  #  This should display properly in ipython.

spectrumPlot.savePdf('/home/raven/Desktop/sdrplay_fft.pdf')

