#Importe todas as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import read, write
from record_module import *
from funcoes_LPF import *
import time

fs = 44100
signal = signalMeu()
sd.default.samplerate = fs
sd.default.channels = 1

def main():
    # Sinal Recebido
    sound_recieved = np.array(read("modulado_leo.wav")[1], dtype=float)
    print(sound_recieved)
    T = int(len(sound_recieved)/fs)
    print(f"O som possui {len(sound_recieved)} amostras e possui {T} segundos")
    signal.plotFFT(sound_recieved, fs, "Fourier - Áudio Recebido")

    # Desmodulado
    portadora = signal.generateSin(20000, 1, T, fs)[1]
    demodulado = portadora*sound_recieved
    signal.plotFFT(demodulado, fs, "Fourier - Áudio Desmodulado")
    # signal.plotSignal(demodulado, T, fs, "Sinal demodulado")
    
    # Filtrado
    filtrado = LPF(demodulado, 4000, fs)
    signal.plotFFT(filtrado, fs, "Fourier - Áudio Recebido Filtrado")


    sd.play(filtrado)
    sd.wait()


if __name__ == "__main__":
    main()