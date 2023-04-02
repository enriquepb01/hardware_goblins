
import paho.mqtt.client as mqtt

import pyaudio
import sys, time
import numpy as np
import wave

from AudioLib.AudioEffect import AudioEffect

# control variables
n = 0
echo = 0
realTime = 1
play = 0
change = 0

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

def extractConfig(configList, mqttString):
    mqttList = mqttString.split(",")
    for item in mqttList:
        if(item[0] == "[" ):
            # extracting n
            configList.append(int(item[1:]))
        elif(item[len(item)-1] == "]"):
            # extracting realtime
            configList.append(item[:len(item)-1])
        else:
           # extracting echo and then play
            configList.append(item)


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



# MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe('goblin/test', 2)
    client.message_callback_add('goblin/test', goblin_callback)

#Default message callback.
def on_message(client, userdata, msg):
    pass

def goblin_callback(client, userdata, msg):
    global n
    global echo
    global realTime
    global play
    global change
    # 4 items in transmission: n, echo (0/1), play (0/1), realtime (0/1)
    data = str(msg.payload, 'utf-8').strip()
    # parse through list of payload, extract the three items shown above
    config = []
    extractConfig(config, data)
    n = int(config[0])
    echo = int(config[1])
    play = int(config[2])
    realTime = int(config[3])

def playSound():
    global n
    global echo
    global play
    global realTime
    while True:
        if(play == 0):
            break
        if(realTime == 0):
            break

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

        if(echo):
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

if __name__ == '__main__':
    #starts mqtt connection
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        if(play == 1 and realTime == 1):
            # add logic
            playSound()
        elif(play == 1 and realTime == 0):
            # add logic for recorded version
            AudioEffect.echo('input_audio.wav', 'echo_audio.wav')
            AudioEffect.darth_vader('input_audio.wav', 'darth_audio.wav')
            AudioEffect.radio('input_audio.wav', 'radio_output.wav')
            AudioEffect.ghost('input_audio.wav', 'ghost_output.wav')

        
        



        
        
        
