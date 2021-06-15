#! /usr/bin/python

import numpy as np
import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyaudio
import struct
from scipy.fftpack import fft
import time

class Audio(object):
    def __init__(self):

        #pyqt
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='Waveform')
        self.win.setWindowTitle('Waveform')
        self.win.setGeometry(5, 115, 1910, 1070)

        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (127, '128'), (255, '255')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])


        self.waveform = self.win.addPlot(
            title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},
        )

        #pyaudio
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels = self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK
        )

        self.x = np.arange(0, 2 * self.CHUNK, 2)


    def start(self):
         if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, 2 * self.CHUNK, padding=0.005)

    def update(self):
        wf_data = self.stream.read(self.CHUNK)
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128
        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data,)


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()
if __name__ == '__main__':

    audio_app = Audio()
    audio_app.animation()