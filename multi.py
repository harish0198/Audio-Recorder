import multiprocessing
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
import wave
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
WAVE_OUTPUT_FILENAME = "recordedFile.wav"
device_index = 2
audio = pyaudio.PyAudio() 

def ps1(index,RECORD_SECONDS):
    i=0
    f,ax = plt.subplots()
    # Prepare the Plotting Environment with random starting values
    x = np.arange(100)
    y = np.random.randn(100)

    # Plot 0 is for raw audio data
    li, = ax.plot(x, y)
    ax.set_xlim(0,550)
    ax.set_ylim(-5000,5000)
    ax.set_title("Raw Audio Signal")
    plt.tight_layout()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = index,
                    frames_per_buffer=CHUNK)

    t_end = time.time() + RECORD_SECONDS
    while time.time() < t_end:
    # do whatever you do
        # get and convert the data to float
        audio_data = np.fromstring(stream.read(CHUNK, exception_on_overflow = False), np.int16)
        li.set_xdata(np.arange(len(audio_data)))
        li.set_ydata(audio_data)
        # Show the updated plot, but without blocking
        plt.pause(0.01)
    plt.close('all')

def ps2(index,RECORD_SECONDS):

    Recordframes=[]
    print ("recording started")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = index,
                    frames_per_buffer=CHUNK)

    t_end = time.time() + RECORD_SECONDS
    while time.time() < t_end:
        data = stream.read(CHUNK, exception_on_overflow = False)
        Recordframes.append(data)

    print ("recording stopped")


    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()

def record(rec_tim):

    index = 1
    print("recording via index "+str(index))


    # creating processes
    p1 = multiprocessing.Process(target = ps1,args = (index,rec_tim))
    p2 = multiprocessing.Process(target = ps2,args = (index,rec_tim))

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()
    
  # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()

    # both processes finished
    print("Done!")

def playback():
    # open the file for reading.
    wf = wave.open('recordedFile.wav', 'rb')

    # open stream based on the wave object which has been input.
    stream = audio.open(format =
                    audio.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read data (based on the chunk size)
    data = wf.readframes(CHUNK)

    # play stream (looping from beginning of file to the end)
    while data:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(CHUNK)
        
if __name__ == '__main__':     
    RECORD_SECONDS = 5

    record(RECORD_SECONDS)