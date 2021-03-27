import time
from utils import *
from datagrama import *
import sys


def get_on_five(size, porta):
    response = porta.rx.getOnTime(size, 5)

    print(f"All Response: {response}")

    if response == False:
        print('Inatividade percebida...')
        print("Não foi recebido uma resposta... Encerrando comunicação")
        mensagem_tipo_5 = Datagrama(5).createDatagrams()
        print(f'Enviando mensagem do tipo 5: {mensagem_tipo_5}')
        porta.sendData(mensagem_tipo_5)
        porta.disable()
        sys.exit()
    
    elif response[0] == 5:
        print('Mensagem do tipo Time Out recebida...')
        print('A comunicação será encerrada!')
        porta.disable()
        sys.exit()
    
    else:
        return response


def get_on_twenty(size, porta):
    tentativas = 1

    while tentativas < 4:
        response = porta.rx.getOnTime(size, 5)
        print(f"All Response: {response}")

        if response == False:
            print('Inatividade percebida...')
            print(f'Tentando novamente [{tentativas}/4]')
            tentativas += 1
            print(f"tentativas {tentativas}")
        
        elif response[0] == 5:
            print('Mensagem do tipo Time Out recebida...')
            print('A comunicação será encerrada!')
            porta.disable()
            sys.exit()
        
        else:
            print('Comunicação reestabelecida com sucesso! ')
            tentativas += 4
            return response
        


    print("Não foi recebido uma resposta... Encerrando comunicação")
    mensagem_tipo_5 = Datagrama(5).createDatagrams()
    print(f'Enviando mensagem do tipo 5: {mensagem_tipo_5}')
    porta.sendData(mensagem_tipo_5)
    porta.disable()
    sys.exit()