#importe as bibliotecas
from numpy.lib.shape_base import column_stack
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import pandas as pd
from suaBibSignal import *
import sys


bib_signal = signalMeu()


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
    
    key = input('Qual tecla você deseja apertar? ')
    freq1, freq2 = frequencies(key)
    print(f'Freqências retornadas: {freq1} e {freq2}')
    
    fs = 44100
    A = 1
    T = 1

    x1, s1 = bib_signal.generateSin(freq1, A, T, fs)
    x2, s2 = bib_signal.generateSin(freq2, A, T, fs)
    s3 = s1 + s2

    sd.play(s3, fs)

    bib_signal.plotSignal(key, s3, T, fs)
    bib_signal.plotFFT(s3, fs)
    
    sd.wait()
    

   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    
    """
    print("Inicializando encoder")
    print("Aguardando usuário")
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(tone, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()
    plotFFT(self, signal, fs)
    """
    

if __name__ == "__main__":
    main()
