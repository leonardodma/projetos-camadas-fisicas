from enlace import *
import time
import numpy as np
import os
import io
import PIL.Image as Image
import sys
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

from utils import *
from utils2 import *
from datagrama import *

#  https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM1"                  # Windows(variacao de)


def main():
    # try:
    com1 = enlace(serialName)
    com1.enable()

    print('A comunicação do cliente foi aberta com sucesso!')
    print('A transmição vai começar')

    # Interface pra escolher imagem
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    imageR = filename
    txBuffer = open(imageR, 'rb').read()
    txLen = len(txBuffer)
    print(f'Tamanho da imagem: {str(txLen)}')

    # Enviando Handshake para ver se servidor está ativo.
    print("Enviando Handshake!...")
    handshake = Datagrama(1, txBuffer).createDatagrams()
    com1.sendData(handshake)
    print('Handshake enviado com sucesso!')

    time.sleep(15)
    # Tentando receber resposta do servidor, para saber se ele está pronto
    handshake_recebido = get_on_five(14, com1)
    print(f'Handshake recebido foi: {handshake_recebido}\n')
    
    # Se não conseguir receber em cinco segundos, tentar novamente
    # Se a mensagem recebida não for do tipo 2, tentar novamente
    while handshake_recebido[0] != int_to_byte(2):
        print('A mensagem recebida do servidor não foi a esperada...')
        print('Tentando reestabelecer comunicação')

        com1.sendData(handshake)
        handshake_recebido = get_on_five(14, com1)
        print(f'Handshake recebido agora foi: {handshake_recebido}')

    print("Servidor respondeu o Handshake! Comunicação estabelecida")

    datagrams = Datagrama(3, txBuffer).createDatagrams()
    print(f"Todos os {len(datagrams)} datagramas foram criados")

    time_start = time.time()

    cont = 1
    for datagram in datagrams:
        print(f"Enviando datagrama: {cont}")
        com1.sendData(datagram)
        print(f"Datagrama {cont} enviado com sucesso")
        print('-----------------------------------------------')

        response = get_on_five(14, com1)
        print(f'Mensagem recebida do servidor: {response}')

        if response[0] == 4:
            print('Recebemos do servidor que o pacote foi recebido com sucesso')
        
        else:
            while response[0] != 4:
                print(f'Ocorreu erro no pacote {response[6]}')
                print('Solicitando reenvio...')
                com1.sendData(datagram)
                response = com1.getData(14)
                print(f"Datagrama {cont} sendo enviado novamente")

        cont += 1


    time_end = time.time()
    print("Transferência finalizou com sucesso!\n")
    transfer_time = time_end - time_start
    taxa_transmissão = txLen/transfer_time

    print("Tempo gasto: {} segundos".format(transfer_time))
    print("Taxa de Transmissão: {} [bytes/s]".format(taxa_transmissão))


    # Encerra comunicação
    print("----------------------------------------------------")
    print("Comunicação encerrada")
    print("----------------------------------------------------")
    com1.disable()
        
    """
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
    """
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()