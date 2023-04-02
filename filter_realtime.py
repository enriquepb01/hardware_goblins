import pyaudio
import sys, time
import numpy as np
import wave
from scipy import signal
from noisereduce.noisereducev1 import reduce_noise

pitch_val = -2    # Pitch shift value (positive is higher pitch, negative is lower pitch)
echo = 1
prev_data, buffer_idx = [0]*(echo*5), 0
full = False
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
swidth = 2
 
p = pyaudio.PyAudio()
 
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = chunk)
 
print("Start")

def pitch_change(n, freq_data):
    filtered_data = [0]*len(freq_data)
    if n >= 0:
        filtered_data[n:len(freq_data)] = freq_data[0:(len(freq_data)-n)]
        filtered_data[0:n] = freq_data[(len(freq_data)-n):len(freq_data)]
    else:
        filtered_data[0:(len(freq_data)+n)] = freq_data[-n:len(freq_data)]
        filtered_data[(len(freq_data)+n):len(freq_data)] = freq_data[0:-n]
    
    return np.array(filtered_data)

def add_echo(n, time_data, prev_data):
    output = time_data
    for val in prev_data:
        output += val
    return output / len(output)

while True:

    time_data = stream.read(chunk)
    time_data = np.array(wave.struct.unpack("%dh"%(len(time_data)/swidth), time_data))
 
    # do real fast Fourier transform 
    freq_data = np.fft.rfft(time_data)
    
    # Filter 1: pitch change
    output_freq = pitch_change(pitch_val, freq_data)
    # output_freq[0:20] = 0
    output_freq[300:513] = 0
    
    # inverse transform to get back to temporal data
    output_time = np.fft.irfft(output_freq)

    # Filter 2: echo
    prev_data[buffer_idx] = output_time
    if buffer_idx + 1 == echo*5:
        buffer_idx = 0
        full = True
    else:
        buffer_idx += 1
    
    if full:
        factor = 0.5
        total = 0
        for val in prev_data:
            output_time += val*factor
            total += factor
            if factor > 0.05:
                factor = factor * 0.3
        
        output_time = output_time / total

    output_time = np.array(output_time, dtype='int16') 
    out_chunk = wave.struct.pack("%dh"%(len(output_time)), *list(output_time)) #convert back to 16-bit data
    stream.write(out_chunk)

