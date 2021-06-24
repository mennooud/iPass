# ! /usr/bin/python
import pyaudio
import struct
import numpy as np
from time import perf_counter
import math

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
    input_device_index=7                                                # selecteer juiste audioinput m.b.v. get_device_info.py voor lagere latency
)

while True:
    # BINARY DATA
    data_bin = stream.read(CHUNK)  # binary data
    data = struct.unpack('{n}h'.format(n=CHUNK), data_bin)              # integer data

    # INTEGER DATA NAAR HERTZ
    x = np.fft.fft(data)                                                # numpy functie voor Fast Fourier Transform algoritme
    freqs = np.fft.fftfreq(len(x))                                      # return
    index = np.argmax(np.abs(x))                                        # index
    freq = freqs[index]
    hz = int(abs(freq * RATE))


    # print(hz)

    # Frequency ranges
    def freq_range():
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        base_note,base_note_frequency, base_note_octave = ('A', 440, 4)
        note_multiplier = 2**(1/len(notes))
        hz_base_note = hz / base_note_frequency

        distance_base_note = math.log(hz_base_note,abs(note_multiplier))
        distance_base_note = round(distance_base_note)

        base_note_index_octave = notes.index(base_note)
        base_note_abs_index = base_note_octave * len(notes) + base_note_index_octave
        note_abs_index = base_note_abs_index + distance_base_note
        note_octave, note_index_octave = note_abs_index // len(notes), note_abs_index % len(notes)
        note_name = notes[note_index_octave]
        note = (note_name, note_octave)

        if hz > 16 and hz < 60:                                         # Sub-bass	        20 to 60 Hz
            print('Sub-bass (' + str(hz) + ' Hz) ' + str(note))
        if hz > 61 and hz < 250:                                        # Bass	            60 to 250 Hz
            print('Bass (' + str(hz) + ' Hz) ' + str(note))
        if hz > 251 and hz < 500:                                       # Low midrange	    250 to 500 Hz
            print('Low midrange (' + str(hz) + ' Hz) ' + str(note))
        if hz > 501 and hz < 2000:                                      # Midrange	        500 Hz to 2 kHz
            print('Midrange (' + str(hz) + ' Hz) ' + str(note))
        if hz > 2001 and hz < 4000:                                     # Upper midrange	2 to 4 kHz
            print('Upper midrange (' + str(hz) + ' Hz) ' + str(note))
        if hz > 4001 and hz < 6000:                                     # Presence	        4 to 6 kHz
            print('Presence (' + str(hz) + ' Hz) ' + str(note))
        if hz > 6001 and hz < 20000:                                    # Brilliance	    6 to 20 kHz
            print('Brilliance (' + str(hz) + ' Hz ' + str(note))

    freq_range()

    def freq_to_notes():
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        multiplier = 2



    kickfreqrange = hz > 201 and hz < 500
    t1 = perf_counter()
    def beats_per_minute():  # bpm calculatie is me niet gelukt
        t = perf_counter()
        bpm = 60 / (t - t1)
        print(bpm)
    # beats_per_minute()

    # play audio
    # stream.write(data_bin)  # comment uit als je underrun errors krijgt.