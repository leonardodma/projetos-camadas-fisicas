#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

from enlace import *
import time
import numpy as np
import os
import io
import PIL.Image as Image
from math import ceil
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename


from utils import *


#  https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM1"                  # Windows(variacao de)


# eop = (4294967295).to_bytes(4, byteorder='big')


def main():
    try:
        com1 = enlace(serialName)
        com1.enable()

        print('A comunicação do cliente foi aberta com sucesso!')
        print('A transmição vai começar')

        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print(filename)
        imageR = filename

        txBuffer = open(imageR, 'rb').read()
        print(f'Imagem: {txBuffer}')


        txLen = len(txBuffer)
        print('txLen: \n' + str(txLen))


        time_start = time.time()

        print("Enviando Handshake!")
        handshake = create_handshake()
        com1.sendData(handshake)
        print("Handshake Enviado! Comunicação estabelecida")



        datagrams = create_datagrams(txBuffer)
        print(f"Todos os {len(datagrams)} datagramas foram criados")

        cont = 1
        for datagram in datagrams:
            print("Enviando datagrama: {}".format(cont))
            com1.sendData(datagram)
            print("Datagrama {} enviado com sucesso".format(cont))
            print('-----------------------------------------------')

            response = com1.getData(14)[0]
            
            type_of_message = response[8:10]
            print(f'Resposta do servidor: {type_of_message}')

            if type_of_message == (3).to_bytes(2, byteorder='big'):
                print('Recebemos do servidor que o primeiro pacote foi enviado com sucesso')
            
            elif type_of_message == (4).to_bytes(2, byteorder='big'):
                user_reponse = input('Um erro ocorreu, deseja tentar novamente?[y/n] ')
                
                if user_reponse == 'y':
                    print('Tentando enviar novamente...')
                    com1.sendData(datagram)
                    break
                else:
                    print('FALHA AO TENTAR ENVIAR IMAGEM :(')
                    break

            cont += 1

        """
        resposta, len_resposta = com1.getData(3)
        print("Resposta: {}".format(resposta) )


        if int.from_bytes(resposta, byteorder='big') == txLen:
            time_end = time.time()
            print("Transferência finalizou com sucesso!")
            transfer_time = time_end - time_start
            taxa_transmissão = txLen/transfer_time

            print("Tempo gasto: {} segundos".format(transfer_time))
            print("Taxa de Transmissão: {} [bytes/s]".format(taxa_transmissão))
        """

        # Encerra comunicação
        print("----------------------------------------------------")
        print("Comunicação encerrada")
        print("----------------------------------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()