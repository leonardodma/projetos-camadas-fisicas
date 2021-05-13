
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import peakutils


class signalMeu:
    def __init__(self):
        self.init = 0

    def generateSin(self, freq, amplitude, time, fs):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier')
        plt.xlabel("frenquência (Hz)")
        plt.ylabel("Amplitude(f)")
        plt.show()

    def plotSignal(self, signal, time, fs, titulo=None):
        n = int(time*fs)
        x = np.linspace(0.0, time, n)
        plt.figure()
        plt.plot(x, signal)

        if titulo == None:
            plt.title("Senoide")
        else:
            plt.title(titulo)
            
        plt.xlabel("tempo (s)")
        plt.ylabel("Amplitude")
        plt.show()
    
    def plotRecieved(self, signal, time, fs):
        n = int(time*fs)
        x = np.linspace(0.0, time, n)
        plt.figure()
        plt.plot(x, signal)
        plt.title(f"Som recebido")
        plt.xlabel("tempo (s)")
        plt.ylabel("Amplitude")
        plt.show()
  