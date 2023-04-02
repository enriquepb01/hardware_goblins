import pyaudio
import sys, time
import numpy as np
import wave

n = -5    # Pitch shift value (positive is higher pitch, negative is lower pitch)
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
    
    # Shift signal for modulation
    filtered_data = [0]*len(freq_data)
    if n >= 0:
        filtered_data[n:len(freq_data)] = freq_data[0:(len(freq_data)-n)]
        filtered_data[0:n] = freq_data[(len(freq_data)-n):len(freq_data)]
    else:
        filtered_data[0:(len(freq_data)+n)] = freq_data[-n:len(freq_data)]
        filtered_data[(len(freq_data)+n):len(freq_data)] = freq_data[0:-n]
    
    freq_data = np.array(filtered_data)
    
    # inverse transform to get back to temporal data
    time_data = np.fft.irfft(time_data)
    output_data = np.array(time_data, dtype='int16') # cast values
    chunkout = wave.struct.pack("%dh"%(len(output_data)), *list(output_data)) #convert back to 16-bit data
    stream.write(chunkout)
 
    
 
print("End Recording")
 
stream.stop_stream()
stream.close()
p.terminate()