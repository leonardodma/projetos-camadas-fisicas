#Importe todas as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import read, write
from record_module import *
from funcoes_LPF import *

fs = 44100
signal = signalMeu()
sd.default.samplerate = fs
sd.default.channels = 1

def main():
    record_to_file('record.wav')

    sound_array = np.array(read("record.wav")[1], dtype=float)
    print(sound_array)

    T = int(len(sound_array)/fs)
    print(f"O som possui {len(sound_array)} amostras e possui {T} segundos")


    maior_valor = np.max(np.abs(sound_array))
    k = 1/maior_valor

    normalizado = k*sound_array
    sd.play(normalizado, fs) # -> ainda com o som audível
    signal.plotSignal(normalizado, T, fs, "Sinal modulado")
    signal.plotFFT(normalizado, fs)

    filtrado = LPF(normalizado, 4000, fs)
    signal.plotFFT(filtrado, fs)
    #sd.play(filtrado, fs)

    portadora = signal.generateSin(20000, 1, T, fs)[1]
    

    modulado = portadora*filtrado
    signal.plotSignal(modulado, T, fs, "Sinal modulado")

    # Write to file 
    write("modulado_leo.wav", fs, modulado)

if __name__ == "__main__":
    main()