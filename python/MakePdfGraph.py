"""
# -*- coding: utf-8 -*-

Created on Wed Nov 28 19:49:28 2018
A Class for Matplotlib using the Object Oriented API.
Specifically for creating PDF graphs for inclusion
in LaTeX documents.

@author: raven
"""

import matplotlib
import numpy as np
matplotlib.use('pdf')
from matplotlib.ticker import EngFormatter

class MakePdfGraph():

    def __init__(self, x, y):
        '''
        x and y are numpy arrays.
        '''
        self.fig = matplotlib.backends.backend_pdf.Figure(figsize=(5, 4), dpi=100)
#        self.fig.add_subplot(111).plot(x, y)
        self.fig.add_axes([0.15,0.15,0.8,0.75], xscale='linear', yscale = 'linear')
        self.ax = self.fig.axes
        self.ax[0].grid(b=True)
        formatter = EngFormatter(unit='Hz')
        self.ax[0].xaxis.set_major_formatter(formatter)
        self.ax[0].set_xlabel('Frequency')
        self.ax[0].set_ylabel('Relative Gain (dB)')
        self.ax[0].set_title('FFT SDRPlay 5 MHz FM Broadcast Band')
        self.ax[0].set_ylim(bottom=-120.0,top=10.0)
        self.ax[0].plot(x,y)
        self.canvas = matplotlib.backends.backend_pdf.FigureCanvasPdf(self.fig)
        
    def reportInternals(self):
        print(f'The current matplotlib backend is {matplotlib.get_backend()}.')
        print(f'Is the current mode interactive? {matplotlib.is_interactive()}')
        #  The default backend is in the matplotlibrc file.
        #  To determine where the file is:
        print(f'The matplotlibrc file is here: {matplotlib.matplotlib_fname()}')
        pass
    
    def display(self):
        '''
        This may have to have backend dependency handled.
        '''
        display(self.fig)
        pass
    
    def savePdf(self, filePath):
        self.fig.savefig(filePath)
        pass
        

#  For testing as a script.  Create a figure using the PDF backend.
if __name__ == '__main__':
    t = np.arange(0, 3, .01)
    y = 2 * np.sin(2 * np.pi * t)
    graph1 = MakePdfGraph(t, y)
    graph1.display()
    graph1.savePdf('/home/raven/sinewave.pdf')
