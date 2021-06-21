# ! /usr/bin/python

import pyaudio
import struct
import numpy as np
import time

# pyaudio
p = pyaudio.PyAudio()
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# audio in
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

while True:
    # binary data
    data = stream.read(CHUNK)
    data_int = struct.unpack('{n}h'.format(n=CHUNK), data)
    data_np = np.array(data_int, dtype='b')[::2] + 128

    # test
    w = np.fft.fft(data_int)
    freqs = np.fft.fftfreq(len(w))
    idx = np.argmax(np.abs(w))
    freq = freqs[idx]
    hz = int(freq * RATE)
    # if hz < 130 and hz > 125:
    # print(hz)

    # Frequency ranges
    '''
    Sub-bass	    20 to 60 Hz
    Bass	        60 to 250 Hz
    Low midrange	250 to 500 Hz
    Midrange	    500 Hz to 2 kHz
    Upper midrange	2 to 4 kHz
    Presence	    4 to 6 kHz
    Brilliance	    6 to 20 kHz
    '''
    def FreqRange():
        if hz > 16 and hz > 60:
            print('Sub-bass')
        if hz > 61 and hz > 250:
            print('Bass')
        if hz > 251 and hz > 500:
            print('Low midrange')
        if hz > 501 and hz > 2000:
            print('Midrange')
        if hz > 2001 and hz > 4000:
            print('Upper midrange')
        if hz > 4001 and hz > 6000:
            print('Presence')
        if hz > 6001 and hz > 20000:
            print('Brilliance')
    FreqRange()

    # play audio
    stream.write(data)
# stream.write(data_np)


