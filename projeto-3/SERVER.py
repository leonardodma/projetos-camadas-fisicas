#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação 2 
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

from CLIENT import client_response
from enlace import *
import time
import numpy as np
import os
import io
import PIL.Image as Image
import sys


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


def continue_runnig(porta):
    # Resposta do Cliente para saber se se vai enviar novamente ou não
    user_response = porta.getData(14)
    type_of_message = user_response[8:10]

    # Se a resposta for 6 - Interromper 
    if type_of_message == (6).to_bytes(2, 'big'):
        print('O CLIENTE INTERROMPEU O ENVIO')
        porta.disable()
        sys.exit()

    # Se o tipo da mensagem for 5 - Tentar novamente.
    elif type_of_message == (5).to_bytes(2, 'big'):
        time.sleep(5) 


def main():
    try:
        com2 = enlace(serialName)
        com2.enable()

        print('A comunicação foi aberta com sucesso!')

        handshake = com2.getData(14) # PRIMEIRO GET REALIAZDO = HANDSHAKE
        com2.sendData(server_response('correct'))

        print(f"Handshake: {handshake}")
        print('Handshake recebido com sucesso! \n')
        print('A comunicação vai começar')

        # Iniciando  algumas variáveis
        final_image = bytearray()
        pacote = 1
        pls = 0
        success = False

        while not success:
            head = com2.getData(10) # SEGUNDO GET REALIAZADO = HEAD

            # ------------------ Declarando variaveis do HEAD, e seus números inteiros ------------------
            ID = head[0:4]
            int_ID = int.from_bytes(ID, byteorder='big')
            print(f'O ID recebido foi: {int_ID}\n')

            number_of_packages = head[4:6]
            int_number_of_packages = int.from_bytes(number_of_packages, byteorder='big')
            print(f'O número total de pacotes será: {int_number_of_packages}\n')

            payload_size = head[6:8]
            int_payload_size = int.from_bytes(payload_size, byteorder='big')
            pls += int_payload_size 
            print(f'Por enquanto, o tamanho total da imagem é: {pls}\n') 

            type_of_message = head[8:10]
            # -------------------------------------------------------------------------------------------

            print('Recebendo payload {}'.format(int_ID))
            payload = com2.getData(int_payload_size) # TERCEIRO GET REALIAZADO = PAYLOAD
            print('Payload {} recebido com sucesso'.format(int_ID))
            print('Recebendo EOP')
            eop = com2.getData(4) # QUARTO GET REALIAZADO = PAYLOAD
            print('EOP recebido com sucesso')

            if int_ID != pacote:
                print('---------------------------------------------------------------------')
                print('UM ERRO OCORREU NA TRANSMISSÃO DA MENSAGEM :(')
                print(f'Era para estar recebendo o pacote {pacote}, mas estou recebendo {int_ID}')
                com2.sendData(server_response('error'))
                print('Mensagem de erro foi enviada ao cliente!\n')

                time.sleep(5)

                continue_runnig(com2)

            elif len(payload) != int_payload_size:
                print('UM ERRO OCORREU NA TRANSMISSÃO DA MENSAGEM :(')
                print('O Payload informado não foi recebido')
                com2.sendData(server_response('error'))
                print('Mensagem de erro enviado ao cliente\n')

                time.sleep(5)
                
                continue_runnig(com2)
            
            else:
                if eop != (4294967295).to_bytes(4, byteorder='big'):
                    print('UM ERRO OCORREU NA TRANSMISSÃO DA MENSAGEM :(')
                    print('O eop não estava na posição correta, ou seja, não ocorreu a transmissão de todos os bytes')
                    com2.sendData(server_response('error'))
                    print('Mensagem de erro enviado ao cliente\n')

                    time.sleep(5)

                    continue_runnig(com2)
                
                else:
                    print('Por enquanto, tudo ocorreu da meneira correta')
                    final_image.extend(payload)
                    # Se nenhum erro ocorrer, enviar que deu certo
                    com2.sendData(server_response('correct'))
                    pacote += 1


            if int_ID == int_number_of_packages:
                print("Último pacote recebido.\n")
                success = True


            
        print(f'Tamanho da imagem recebida: {len(final_image)}')
        print('Salvando dados dos arquivos.\n')
        print(f'Imagem Recebida: {final_image}')
        
        imageW = './img/recebidaCopia.jpg'
        f = open(imageW, 'wb')
        f.write(final_image)

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
