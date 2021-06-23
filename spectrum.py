#! /usr/bin/python

import pyaudio
import struct
import numpy as np
import time

CHUNK = 512 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data input
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

print('stream started')

while True:
    # binary data
    data = stream.read(CHUNK)
    # play audio
    stream.write(data)