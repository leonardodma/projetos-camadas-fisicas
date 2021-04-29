
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
        indexes = peakutils.peak.indexes(y, thres=0.2, min_dist=10, thres_abs=False)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.plot(x[indexes], y[indexes], marker="o", ls="", ms=3)
        plt.title('Fourier')
        plt.xlabel("frenquência (Hz)")
        plt.ylabel("Frequência de cada frequência")

        for idx in indexes:
            plt.annotate(f"{x[idx]:.2f}[Hz]", (x[idx], y[idx]))

        plt.show()

    def plotSignal(self, key, signal, time, fs):
        n = int(time*fs)
        x = np.linspace(0.0, time, n)
        plt.figure()
        plt.plot(x[:500], signal[:500])
        plt.title(f"Senoide da tecla {key}")
        plt.show()
    
    def plotRecieved(self, signal, time, fs):
        n = int(time*fs)
        x = np.linspace(0.0, time, n)
        plt.figure()
        plt.plot(x, signal)
        plt.title(f"Som recebido")
        plt.xlabel("tempo (s)")
        plt.ylabel("frenquência (Hz)")
        plt.show()

    def getFrequences(self, signal, fs):
        x, y = self.calcFFT(signal, fs)
        indexes = peakutils.peak.indexes(y, thres=0.2, min_dist=10, thres_abs=False)
        print(indexes)

        if len(indexes) == 2:
            return x[indexes]
        
        else:
            return [x[indexes[0]], x[indexes[-1]]]
                

            