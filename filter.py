import pyaudio
import sys, time
import numpy as np
import wave

n = 10    # Pitch shift value (positive is higher pitch, negative is lower pitch)
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
 
start = time.time()
while True:
 
    time_data = stream.read(chunk)
    time_data = np.array(wave.struct.unpack("%dh"%(len(time_data)/swidth), time_data))
 
    # do real fast Fourier transform 
    freq_data = np.fft.rfft(time_data)
    
    # This does the shifting
    filtered_data = [0]*len(freq_data)
    if n >= 0:
        filtered_data[n:len(freq_data)] = freq_data[0:(len(freq_data)-n)]
        filtered_data[0:n] = freq_data[(len(freq_data)-n):len(freq_data)]
    else:
        filtered_data[0:(len(freq_data)+n)] = freq_data[-n:len(freq_data)]
        filtered_data[(len(freq_data)+n):len(freq_data)] = freq_data[0:-n]
    
    output_freq = np.array(filtered_data)
    # Done shifting
    
    # inverse transform to get back to temporal data
    output_time = np.fft.irfft(output_freq)
    
    output_time = np.array(output_time, dtype='int16') 
    out_chunk = wave.struct.pack("%dh"%(len(output_time)), *list(output_time)) #convert back to 16-bit data
    stream.write(out_chunk)
