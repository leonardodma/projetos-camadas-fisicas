#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação 2 
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

from enlace import *
import time
import numpy as np
import os
import io
import PIL.Image as Image


from utils import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM2"                  # Windows(variacao de)


eop = (4294967295).to_bytes(4, byteorder='big')
zero_byte = (0).to_bytes(2, 'big')

def server_response(response):
    if response == 'error':
        msg_type = (4).to_bytes(2, 'big')

    elif response == 'correct':
        msg_type = (3).to_bytes(2, 'big')

    head = create_head((0).to_bytes(4, 'big'), zero_byte, zero_byte, msg_type)
    datagram = head + eop

    return datagram




def main():
    try:
        com2 = enlace(serialName)
        com2.enable()

        print('A comunicação foi aberta com sucesso!')
        print('A recepção vai começar')

        handshake, len_handshake = com2.getData(14) # PRIMEIRO GET REALIAZDO = HANDSHAKE
        print(f"Handshake: {handshake}")
        print('Handshake recebido com sucesso!')
        print('A comunicação vai começar')

        final_image = bytearray()
        pacote = 1

        pls = 0

        boolean = True
        while boolean:
            head, len_head = com2.getData(10) # SEGUNDO GET REALIAZADO = HEAD

            # ------------------ Declarando variaveis do HEAD, e seus numeros inteiros ------------------
            ID = head[0:4]
            int_ID = int.from_bytes(ID, byteorder='big')

            number_of_packages = head[4:6]
            int_number_of_packages = int.from_bytes(number_of_packages, byteorder='big')
            print(f'O número total de pacotes será: {int_number_of_packages}')

            payload_size = head[6:8]
            int_payload_size = int.from_bytes(payload_size, byteorder='big')
            pls += int_payload_size
            print(f'Por enquanto, o tamnho do Pyload é: {pls}')

            type_of_message = head[8:10]
            int_type_of_message = int.from_bytes(type_of_message, byteorder='big')
            # -------------------------------------------------------------------------------------------

            if int_ID != pacote:
                print('UM ERRO OCORREU NA TRANSMISSÃO DA MENSAGEM :(')
                print(f'Era para estar recebendo o pacote {pacote}, mas estou recebendo {int_ID}\n')
                com2.sendData(server_response('error'))
                

            print('Recebendo pacote {}'.format(int_ID))

            payload, len_payload = com2.getData(int_payload_size) # TERCEIRO GET REALIAZADO = PAYLOAD
            print('Recebi pacote {}\n'.format(int_ID))
            final_image.extend(payload)
            

            eop = com2.getData(4)[0] # QUARTO GET REALIAZADO = PAYLOAD
            if eop != (4294967295).to_bytes(4, byteorder='big'):
                print('UM ERRO OCORREU NA TRANSMISSÃO DA MENSAGEM :(')
                com2.sendData(server_response('error'))

            com2.sendData(server_response('correct'))


            if int_ID == int_number_of_packages:
                print("Último pacote recebido.\n")
                boolean = False

            pacote += 1

            
        print(f'Tamanho da imagem recebida: {len(final_image)}')
        print('Salvando dados dos arquivos.\n')
        print(f'Imagem Recebida: {final_image}')
        
        imageW = './img/recebidaCopia.jpg'
        f = open(imageW, 'wb')
        f.write(final_image)
        # https://stackoverflow.com/questions/25831710/convert-a-list-of-bytes-to-a-byte-string)


        print("Imagem salva com sucesso")
            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
