from enlace import *
from datagrama import *
import time

def int_to_byte(number):
    byte_number = (number).to_bytes(1, 'big')
    return byte_number


def byte_to_int(byte):
    number = int.from_bytes(byte, byteorder='big')
    return number


def get_on_five(size, porta):
    time.sleep(10)
    response = porta.rx.getOnTime(size, 5)

    if byte_to_int(response[0]) == 5:
        print('Mensagem do tipo Time Out recebida...')
        print('A comunicação será encerrada!')
        porta.disable()

    elif response == False:
        print('Inatividade percebida...')
        print("Não foi recebido uma resposta... Encerrando comunicação")
        mensagem_tipo_5 = Datagrama(5).createDatagrams()
        print(f'Enviando mensagem do tipo 5: {mensagem_tipo_5}')
        porta.sendData(mensagem_tipo_5)
        porta.disable()
    
    return response