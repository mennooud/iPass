# ! /usr/bin/python
import pyaudio
import struct
import numpy as np
from time import perf_counter
import matplotlib.pyplot as plt
from scipy.fftpack import fft

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
    input_device_index=7                                # selecteer juiste audioinput m.b.v. get_device_info.py voor lagere latency
)

# MATPLOTLIB
y = np.linspace(0, RATE, CHUNK)                         # x-variabele voor plotting

fig, ax = plt.subplots(1, figsize=(15, 7))              # matplotlib afmetingen en assen
line2d = plt.plot()

line_fft, = ax.semilogx(                                # x as in semilogx
    y, np.random.rand(CHUNK), '-', lw=2)

plt.setp(ax, yticks=[0, 1], )                           # hoogte y-as

ax.set_xlim(20, RATE / 2)                               # format spectrum axes

mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(5, 120, 1910, 1070)
plt.show(block=False)

frame_count = 0

while True:
    # BINARY DATA
    data_bin = stream.read(CHUNK)                                   # binary data
    data = struct.unpack('{n}h'.format(n=CHUNK), data_bin)          # integer data

    # INTEGER DATA NAAR HERTZ
    x = np.fft.fft(data)                                            # numpy functie voor Fast Fourier Transform algoritme
    freqs = np.fft.fftfreq(len(x))                                  # return
    index = np.argmax(np.abs(x))                                    # index
    freq = freqs[index]
    hz = int(freq * RATE)
    # print(hz)

    # MATPLOTLIB
    yf = fft(data)                                                  # updaten van line
    line_fft.set_ydata(
        np.abs(yf[0:CHUNK]) / (128 * CHUNK))

    fig.canvas.draw()                                               # update figure canvas
    fig.canvas.flush_events()
    frame_count += 1




    # FREQUENCY RANGES
    def freq_range():

        if hz > 16 and hz < 60:                                         # Sub-bass	        20 to 60 Hz
            print('Sub-bass (' + str(hz) + ' Hz)')
        if hz > 61 and hz < 250:                                        # Bass	            60 to 250 Hz
            print('Bass (' + str(hz) + ' Hz)')
        if hz > 251 and hz < 500:                                       # Low midrange	    250 to 500 Hz
            print('Low midrange (' + str(hz) + ' Hz)')
        if hz > 501 and hz < 2000:                                      # Midrange	        500 Hz to 2 kHz
            print('Midrange (' + str(hz) + ' Hz)')
        if hz > 2001 and hz < 4000:                                     # Upper midrange	2 to 4 kHz
            print('Upper midrange (' + str(hz) + ' Hz)')
        if hz > 4001 and hz < 6000:                                     # Presence	        4 to 6 kHz
            print('Presence (' + str(hz) + ' Hz)')
        if hz > 6001 and hz < 20000:                                    # Brilliance	    6 to 20 kHz
            print('Brilliance (' + str(hz) + ' Hz)')


    freq_range()

    '''
    kickfreqrange = hz > 201 and hz < 500
    t1 = perf_counter()
    def beats_per_minute():  # bpm calculatie is me niet gelukt
        t = perf_counter()
        bpm = 60 / (t - t1)
        print(bpm)
  # beats_per_minute()
    '''

    # play audio
    # stream.write(data_bin)                    # comment uit als je underrun errors krijgt.

