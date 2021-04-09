from enlace import *
import time
import numpy as np
import os
import io
import PIL.Image as Image
import sys
from crcmod import *
from utils import *
from utils2 import *
from datagrama import *
crc16 = mkCrcFun(0x11021, initCrc=0, xorOut=0xFFFFFFFF)

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
    print(com2.fisica.name)
    com2.enable()

    print('A comunicação foi aberta com sucesso!\n')

    # Recebe um handshake e envia a resposta ao cliente.
    handshake = com2.getData(14)

    write_server_log(create_log('get', handshake[0], len(handshake)))
    print(f"Handshake: {handshake}")
    
    type2 = Datagrama(2).createDatagrams()
    print(f'Enviando mensagem do tipo 2: {type2}')

    if handshake[0] == 1:
        time.sleep(1)
        print('Handshake recebido com sucesso! \n')

        # time.sleep(50) # Para simular erro de time out handshake

        com2.sendData(type2)
        write_server_log(create_log('send', type2[0], len(type2)))
        print('A comunicação vai começar')
    else:
        while handshake[0] != 1:
            # tenta receber o handshake novamente
            handshake = com2.getData(14)
            write_server_log(create_log('get', handshake[0], len(handshake)))

            com2.sendData(type2)
            write_server_log(create_log('send', type2[0], len(type2)))

            time.sleep(1)


    # Iniciando  algumas variáveis
    final_image = bytearray()
    pacote = 1
    success = False

    while not success:
        head = get_on_time(10, com2) # SEGUNDO GET REALIAZADO = HEAD
        # ------------------ Declarando variaveis do HEAD, e seus números inteiros ------------------
        number_of_packages = head[3]
        ID = head[4]
        print(f'O ID recebido foi: {ID}\n')
        payload_size = head[5]
        crc_client = head[8:10]

        # -------------------------------------------------------------------------------------------

        print('Recebendo payload {}...'.format(ID))
        payload = com2.getData(payload_size) # TERCEIRO GET REALIAZADO = PAYLOAD
        print('Payload {} recebido com sucesso'.format(ID))
        crc_server = crc16(payload).to_bytes(2, "big")

        print('Recebendo EOP...')
        eop = com2.getData(4) # QUARTO GET REALIAZADO = PAYLOAD
        print('EOP recebido com sucesso')
        write_server_log(create_log('get', head[0], len(head) + len(payload) + len(eop)))

        
        """ # Simular erro de pacote

        print(f'Passou 20 segundos? {have_passed()}')
        if not have_passed():
            pacote = 1
        else:
            if pacote <= 1:
                pacote = 2
            else:
                pacote = pacote
            print(f'PACOTE: {pacote}')
        """
        
        if ID != pacote or len(payload) != payload_size or eop != (4294967295).to_bytes(4, byteorder='big') or crc_client!= crc_server:
            print('----------------------------------------------------------------------------')
            print('UM ERRO OCORREU NA TRANSMISSÃO DA MENSAGEM :(')

            if ID != pacote:
                print(f'Era para estar recebendo o pacote {pacote}, mas recebi {ID}')

            elif len(payload) != payload_size:
                print(f'Os tamanhos do payload informado e recebido devirgiram.')
            
            elif crc_client!= crc_server:
                print("Os CRCs não bateram... Algum bit foi perdido!")
            
            else:
                print('O payload não foi recebido corretamente')

            error_massage = Datagrama(6, ID).createDatagrams()
            com2.sendData(error_massage)
            write_server_log(create_log('send', 6, len(error_massage), error_massage[6]))
            print('Mensagem de erro foi enviada ao cliente!\n')
            time.sleep(5)

        
        elif head[0] == 3:
            time.sleep(1)
            print('Por enquanto, tudo ocorreu da meneira correta')
            final_image.extend(payload)
            # Se nenhum erro ocorrer, enviar que deu certo
            correct_massege = Datagrama(4, pacote).createDatagrams()

            # time.sleep(50) # Para simular erro de time out

            """ Para simular erro de retirada de fios
            while not have_passed():
                time.sleep(1)
            else:
                com2.sendData(correct_massege)
            """

            com2.sendData(correct_massege)

            write_server_log(create_log('send', correct_massege[0], len(correct_massege)))
            print('Mensagem de sucesso enviado ao cliente!')

            pacote += 1

        if ID == number_of_packages:
            print("Último pacote recebido.\n")
            success = True

        
    print(f'Tamanho da imagem recebida: {len(final_image)}')
    print('Salvando dados dos arquivos.\n')
    print(f'Imagem Recebida: {final_image}')
    
    imageW = './img/recebidaCopia.png'
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
