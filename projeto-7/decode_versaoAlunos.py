
#Importe todas as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import read
from record_module import *
import pandas as pd


teclado = {}
teclado["Freq"] = [697, 770, 852, 941]
teclado[1209] = ["1", "4", "7", "X"]
teclado[1336] = ["2", "5", "8", "0"]
teclado[1477] = ["3", "6", "9", "#"]
teclado[1633] = ["A", "B", "C", "D"]
tabela_teclado = pd.DataFrame(teclado).set_index("Freq")


#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def getKey(freq_menor, freq_maior):
    freqs_menores = tabela_teclado.index
    menor = min(freqs_menores, key=lambda x:abs(x-freq_menor))

    freqs_maiores = tabela_teclado.columns
    maior = min(freqs_maiores, key=lambda x:abs(x-freq_maior))

    return int(tabela_teclado.loc[[menor]][maior].values[0])


def main():
    fs = 44100

    bib_signal = signalMeu()
    sd.default.samplerate = fs
    sd.default.channels = 1 #Tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com1.


    record_to_file('beep.wav')
    # https://stackoverflow.com/questions/16778878/python-write-a-wav-file-into-numpy-float-array

    sound_array = np.array(read("beep.wav")[1], dtype=float)
    myrecording = sound_array
    sd.play(myrecording, fs)
    # myrecording = sd.playrec(sound_array, fs)
    
    T = len(myrecording)/fs
    print(f"O som possui {len(myrecording)} amostras e possui {T} segundos")
    
    bib_signal.plotRecieved(myrecording, T, fs)
    bib_signal.plotFFT(sound_array, fs)

    freq1, freq2 = bib_signal.getFrequences(sound_array, fs)
    print(f"Frequências retornadas: {freq1}[Hz] e {freq2}[Hz]")
    print(f"A tecla apertada no teclado foi: {getKey(freq1, freq2)}")
    

if __name__ == "__main__":
    main()
