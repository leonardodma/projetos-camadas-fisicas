#importe as bibliotecas
from numpy.lib.shape_base import column_stack
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import pandas as pd
from suaBibSignal import *
import sys


teclado = {}
teclado["Freq"] = [697, 770, 852, 941]
teclado[1209] = ["1", "4", "7", "X"]
teclado[1336] = ["2", "5", "8", "0"]
teclado[1477] = ["3", "6", "9", "#"]
teclado[1633] = ["A", "B", "C", "D"]
tabela_teclado = pd.DataFrame(teclado).set_index("Freq")


def frequencies(key):
    for index, values in tabela_teclado.items():
        for element in values:
            if element == key:
                maior = index

    menor = tabela_teclado.index[tabela_teclado[maior] == key].tolist()[0]
    
    return menor, maior


#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)


#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    fs = 44100
    A = 1
    T = 1
    bib_signal = signalMeu()
    sd.default.samplerate = fs
    sd.default.channels = 1 #Tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com1.
    
    key = input('Qual tecla você deseja apertar? ')
    freq1, freq2 = frequencies(key)
    print(f'Freqências retornadas: {freq1} e {freq2}')
    

    x1, s1 = bib_signal.generateSin(freq1, A, T, fs)
    x2, s2 = bib_signal.generateSin(freq2, A, T, fs)
    s3 = s1 + s2

    print(s3)

    som_gravado = []
    for value in s3:
        som_gravado.append(str(value))

    sd.play(s3, fs)

    bib_signal.plotSignal(key, s3, T, fs)
    bib_signal.plotFFT(s3, fs)
    sd.wait()

    with open(f"signal.txt", "w") as file:
        file.write(" ".join(som_gravado))
    

if __name__ == "__main__":
    main()
