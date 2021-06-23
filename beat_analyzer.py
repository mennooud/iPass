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
    freq_in_hertz = abs(freq * 11025.0)
    # if freq_in_hertz < 5000 and freq_in_hertz > 100:
    print(freq_in_hertz)

    # play audio
    stream.write(data)
# stream.write(data_np)
