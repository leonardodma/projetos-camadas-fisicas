from enlace import *
import numpy as np
import PIL.Image as Image
from math import ceil


eop = (4294967295).to_bytes(4, byteorder='big')


def create_head(ID, number_of_packages, payload_size, msg_type):
    # ID = Qual Mensagem está sendo enviada 
    # Número de pacotes que serão enviados
    # Tamanho do payload
    # msg_type -> 1 = (Handshake), 2 = (Envio da Imagem), 3 = (Sucesso), 4 = (Erro)
    head = ID +  number_of_packages + payload_size + msg_type
    return head


def create_handshake():
    zero_byte = (0).to_bytes(2, 'big')
    msg_handshake = (1).to_bytes(2, 'big') # 1 para enviar o handshake
    
    head = create_head((0).to_bytes(4, 'big'), zero_byte, zero_byte, msg_handshake)

    datagrama = head + eop

    return datagrama  


def create_datagrams(message):
    print(f'O tamanho da imagem recebido é: {len(message)}')

    datagrams = []

    # ID da mensagem
    ID = 1 # Primeiro pacote terá o ID = 1

    # Número de pacotes 
    number_of_packages = ceil(len(message)/114) # ceil = arredondar para cima
    number_of_packages_byte = (number_of_packages).to_bytes(2, byteorder='big')
    print(f'Serão enviados {number_of_packages} pacotes')

    # Tipo da Mensagem
    msg_img = (2).to_bytes(2, 'big') # 2 para enviar a imagem

    for i in range(0, len(message), 114):
        print(i)
        if len(message) - i >= 114:
            payload = message[0+i : 114+i]
            payload_size_byte = (len(payload)).to_bytes(2, byteorder='big')
            print(f'O tamanho do Payload do datagrama {ID} é: {len(payload)}')


        else:
            payload = message[i:]
            print(f'O tamanho do último Payload (Datagrama {ID}) é: {len(payload)}')
            payload_size_byte = (len(payload)).to_bytes(2, byteorder='big')
        
        
        ID_bytes = ID.to_bytes(4, byteorder='big')
        head = create_head(ID_bytes, number_of_packages_byte, payload_size_byte, msg_img)
        datagram = head + payload + eop
        datagrams.append(datagram)

        print(f"Datagrama {ID}: {datagram}\n")

        ID += 1

    
    return datagrams