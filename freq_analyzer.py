# ! /usr/bin/python
import sys

import pyaudio
import struct
import numpy as np
import wave
from time import perf_counter


# PYAUDIO
p = pyaudio.PyAudio()
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# AUDIO IN
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK,
    input_device_index=7                                        # selecteer juiste audioinput m.b.v. get_device_info.py voor lagere latency
)

while True:
    # BINARY DATA
    data = stream.read(CHUNK)                                   # binary data

    data_int = struct.unpack('{n}h'.format(n=CHUNK), data)      # integer data
    #data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    data_np = np.array(data_int, dtype='b')[::2] + 128          # data in array


    # binary data to Hertz
    w = np.fft.fft(data_int)                                    # numpy functie voor Fast Fourier Transform algoritme
    freqs = np.fft.fftfreq(len(w))                              # return
    idx = np.argmax(np.abs(w))                                  # index
    freq = freqs[idx]
    hz = int(freq * RATE)
    # if hz < 130 and hz > 125:
    # print(hz)


    # Frequency ranges
    def freq_range():
        '''
        Sub-bass	    20 to 60 Hz
        Bass	        60 to 250 Hz
        Low midrange	250 to 500 Hz
        Midrange	    500 Hz to 2 kHz
        Upper midrange	2 to 4 kHz
        Presence	    4 to 6 kHz
        Brilliance	    6 to 20 kHz
        '''


        if hz > 16 and hz < 60:
            print('Sub-bass ('+ str(hz) +' Hz)')
        if hz > 61 and hz < 250:
            print('Bass ('+ str(hz) +' Hz)')
        if hz > 251 and hz < 500:
            print('Low midrange ('+ str(hz) +' Hz)')
        if hz > 501 and hz < 2000:
            print('Midrange ('+ str(hz) +' Hz)')
        if hz > 2001 and hz < 4000:
            print('Upper midrange ('+ str(hz) +' Hz)')
        if hz > 4001 and hz < 6000:
            print('Presence ('+ str(hz) +' Hz)')
        if hz > 6001 and hz < 20000:
            print('Brilliance ('+ str(hz) +' Hz)')
        

    #freq_range()
    def beats_per_minute():
        if hz > 130 and hz < 500:
            print('kickdrum')
    beats_per_minute()
    # play audio
    stream.write(data)
    #stream.write(data_np)


