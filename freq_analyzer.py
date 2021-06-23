# ! /usr/bin/python
import pyaudio
import struct
import numpy as np
from time import perf_counter


# PYAUDIO
p = pyaudio.PyAudio()
CHUNK = 1024 * 4
WIDTH = 2
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
    data_bin = stream.read(CHUNK)                                   # binary data
    data = struct.unpack('{n}h'.format(n=CHUNK), data_bin)          # integer data

    # INTEGER DATA NAAR HERTZ
    x = np.fft.fft(data)                                        # numpy functie voor Fast Fourier Transform algoritme
    freqs = np.fft.fftfreq(len(x))                              # return
    index = np.argmax(np.abs(x))                                # index
    freq = freqs[index]
    hz = int(freq * RATE)
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
        

    freq_range()

    kickfreqrange = hz > 201 and hz < 500
    t1 = perf_counter()
    def beats_per_minute():                                     # bpm calculatie is me niet gelukt
        t = perf_counter()
        bpm = 60 / (t - t1)
        print(bpm)

    # beats_per_minute()

    # play audio
    stream.write(data_bin)                                      # comment uit als je underrun errors krijgt.


