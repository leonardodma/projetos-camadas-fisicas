from enlace import *
import time
import numpy as np
import os
import io
import PIL.Image as Image
import sys


from utils import *
from utils2 import *
from datagrama import *


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM2"                  # Windows(variacao de)


def main():
    com2 = enlace(serialName)
    com2.enable()

    print('A comunicação foi aberta com sucesso!\n')

    # Recebe um handshake e envia a resposta ao cliente.
    time.sleep(15)
    
    handshake = get_on_five(14, com2)
    print(f"Handshake: {handshake}")
    
    type2 = Datagrama(2).createDatagrams()

    if handshake[0] == 1:
        print('Handshake recebido com sucesso! \n')
        com2.sendData(type2)
        print('A comunicação vai começar')
    else:
        while handshake[0] != 1:
            # tenta receber o handshake novamente
            handshake = get_on_five(14, com2)
            com2.sendData(type2)


    # Iniciando  algumas variáveis
    final_image = bytearray()
    pacote = 1
    success = False

    while not success:
        head = get_on_five(10, com2) # SEGUNDO GET REALIAZADO = HEAD

        # ------------------ Declarando variaveis do HEAD, e seus números inteiros ------------------
        number_of_packages = head[3]
        print(f'O número total de pacotes será: {byte_to_int(number_of_packages)}\n')

        ID = head[4]
        int_ID = byte_to_int(ID)
        print(f'O ID recebido foi: {int_ID}\n')

        payload_size = head[5]
        int_payload_size = byte_to_int(payload_size)
        # -------------------------------------------------------------------------------------------

        print('Recebendo payload {}'.format(int_ID))
        payload = com2.getData(int_payload_size - 1) # TERCEIRO GET REALIAZADO = PAYLOAD
        print('Payload {} recebido com sucesso'.format(int_ID))

        print('Recebendo EOP')
        eop = get_on_five(4, com2) # QUARTO GET REALIAZADO = PAYLOAD
        print('EOP recebido com sucesso')

        if int_ID != pacote or len(payload) != int_payload_size or eop != (4294967295).to_bytes(4, byteorder='big'):
            print('---------------------------------------------------------------------')
            print('UM ERRO OCORREU NA TRANSMISSÃO DA MENSAGEM :(')

            if int_ID != pacote:
                print(f'Era para estar recebendo o pacote {pacote}, mas recebi {int_ID}')

            elif len(payload) != int_payload_size:
                print(f'Os tamanhos do payload informado e recebido devirgiram.')
            
            else:
                print('O payload estava não foi recebido corretamente')


            com2.sendData(Datagrama(6, pacote).createDatagrams())
            print('Mensagem de erro foi enviada ao cliente!\n')
            time.sleep(5)

        
        else:
            print('Por enquanto, tudo ocorreu da meneira correta')
            final_image.extend(payload)
            # Se nenhum erro ocorrer, enviar que deu certo
            com2.sendData(Datagrama(4, pacote))
            pacote += 1


        if int_ID == byte_to_int(number_of_packages):
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
        
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
