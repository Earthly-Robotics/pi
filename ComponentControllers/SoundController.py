import pyaudio
import numpy as np
import pylab
import time

import matplotlib.pyplot as plt


# from Network.ConfigReader import config


class SoundController:
    listening = False

    def __init__(self):
        self.network_controller = None
        # self.params = config()
        # self.ip_address = self.params['ip_address']
        # self.port = int(self.params['port'])
        np.set_printoptions(suppress=True)  # don't use scientific notation
        self.listening = True
        self.CHUNK = 4096  # number of data points to read at a time
        self.RATE = 44100  # time resolution of the recording device (Hz)

        self.p = pyaudio.PyAudio()  # start the PyAudio class
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  input_device_index=2,
                                  frames_per_buffer=self.CHUNK)  # uses default input device

    def get_beat(self):
        print('test')
        while self.listening:
            data = np.fromstring(self.stream.read(self.CHUNK, exception_on_overflow=False), dtype=np.int16)
            data = data * np.hanning(len(data))  # smooth the FFT by windowing data
            fft = abs(np.fft.fft(data).real)
            fft = fft[:int(len(fft) / 2)]  # keep only first half
            freq = np.fft.fftfreq(self.CHUNK, 1.0 / self.RATE)
            freq = freq[:int(len(freq) / 2)]  # keep only first half
            # freqMin = freq[np.where(fft == np.min(fft))[0][0]] + 1
            freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1
            # print("freqency: %d Hz" % freq)
            # print("min frequency: %d Hz" % freqMin)
            print("peak frequency: %d Hz" % freqPeak)

            # uncomment this if you want to see what the freq vs FFT looks like
            # plt.plot(freq,fft)
            # plt.axis([0,4000,None,None])
            # plt.show()
            # plt.close()

        # close the stream gracefully
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def stop_sending(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.listening = False
