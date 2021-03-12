#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

from enlace import *
import time
import numpy as np
import os
import io
import PIL.Image as Image
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

#  https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM1"                  # Windows(variacao de)


"""
Estrutura do Head:
- 10 bytes 

- Id
- Tipo da Mensagem: handshake, dados, erro
- Tamanho do Payload
- Tamanho da Mensagem 
"""

"""
def create_handshake():
    head = create_head((0).to_bytes(2, 'big'), (0).to_bytes(2, 'big'), (0).to_bytes(2, byteorder='big'), mt_handshake)
    datagrama = head + eop
    return datagrama  
"""

def create_head(id, msg_type, msg_size, payload_size):
    head = id + msg_type + msg_size + payload_size
    return head


def create_datagram(message):
    pass


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
        txLen = len(txBuffer)
        print('txLen: \n' + str(txLen))


        # Enviando o head (tamanho do arquivo)
        time_start = time.time()
        tamanho_bytes = (txLen).to_bytes(3, byteorder='big')
        print("Tamnho em bytes {}".format(tamanho_bytes))
        com1.sendData(tamanho_bytes)
        

        # Enviando o arquivo
        print("Cliente mandando o tamanho da imagem para o servidor.")
        com1.sendData(txBuffer)
        print("Cliente mandando a imagem")


        resposta, len_resposta = com1.getData(3)
        print("Resposta: {}".format(resposta) )


        if int.from_bytes(resposta, byteorder='big') == txLen:
            time_end = time.time()
            print("Transferência finalizou com sucesso!")
            transfer_time = time_end - time_start
            taxa_transmissão = txLen/transfer_time

            print("Tempo gasto: {} segundos".format(transfer_time))
            print("Taxa de Transmissão: {} [bytes/s]".format(taxa_transmissão))

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