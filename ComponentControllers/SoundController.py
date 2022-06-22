import pyaudio
import numpy as np
import pylab
import time

import matplotlib.pyplot as plt


# from Network.ConfigReader import config


class SoundController:
    listening = False

    def __init__(self):
        self.diff_pre = 0.5
        self.time_pre = 0.0
        self.counter = 0
        self.alpha = 0.8
        self.n_buff = 8

        self.network_controller = None
        # self.params = config()
        # self.ip_address = self.params['ip_address']
        # self.port = int(self.params['port'])
        np.set_printoptions(suppress=True)  # don't use scientific notation
        self.sending = True
        self.CHUNK = 4096  # number of data points to read at a time
        self.RATE = 44100  # time resolution of the recording device (Hz)

        self.p = pyaudio.PyAudio()  # start the PyAudio class
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)  # uses default input device

    def get_frequency(self):
        """
        Gets frequency
        :return: frequency peak
        """

        while self.sending:
            data = np.fromstring(self.stream.read(self.CHUNK, exception_on_overflow=False), dtype=np.int16)
            data = data * np.hanning(len(data))  # smooth the FFT by windowing data
            fft = abs(np.fft.fft(data).real)
            fft = fft[:int(len(fft) / 2)]  # keep only first half
            freq = np.fft.fftfreq(self.CHUNK, 1.0 / self.RATE)
            freq = freq[:int(len(freq) / 2)]  # keep only first half
            freq_min = freq[np.where(fft == np.min(fft))[0][0]] + 1
            freq_peak = freq[np.where(fft == np.max(fft))[0][0]] + 1
            # print("frequency: %d Hz" % freq)
            # print("min frequency: %d Hz" % freq_min)
            print("peak frequency: %d Hz" % freq_peak)
            return freq_peak

            # uncomment this if you want to see what the freq vs FFT looks like
            # plt.plot(freq,fft)
            # plt.axis([0,4000,None,None])
            # plt.show()
            # plt.close()

    def __reset(self):
        self.counter = 0
        self.diff_pre = 0.5
        return 120

    def __calc(self):
        """
        Calculates bpm
        :return: bpm
        """
        time_cur = time.time()
        if self.counter > 0:
            diff = time_cur - self.time_pre
            if diff > 3.0:
                bpm = self.__reset()
            else:
                if diff > 1.0:
                    diff = 1.0
                elif diff < 0.20:
                    diff = 0.20
                diff = self.alpha * diff + \
                       (1.0 - self.alpha) * self.diff_pre
                bpm = 60 / diff
                self.diff_pre = diff
        else:
            bpm = self.__reset()

        self.time_pre = time_cur
        return bpm

    def bpm_count(self):
        """
        Gets bpm
        :return: bpm
        """
        counter = self.counter
        bpm = self.__calc()

        idx = counter % self.n_buff
        if counter == 0:
            self.bpms = np.array([bpm for k in range(self.n_buff)])
        else:
            self.bpms[idx] = bpm
        bpm_mean = int(np.mean(self.bpms) * 10) // 10

        self.counter += 1
        # print("bpm_mean: " + str(bpm_mean))
        # print("counter: " + str(counter))
        return bpm_mean  # , counter

    def stop_sending(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.sending = False
