from scipy.io import wavfile
import sounddevice as sd

# read data into array
sample_rate, data = wavfile.read('dorime.wav')

# output data
sd.play(data, sample_rate)