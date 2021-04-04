import time
from utils import *
from datagrama import *
import sys
from datetime import datetime


class TimedValue:
    def __init__(self):
        self._started_at = datetime.utcnow()

    def __call__(self):
        time_passed = datetime.utcnow() - self._started_at
        if time_passed.total_seconds() > 40:
            return True
        return False

packge_time = TimedValue()

def have_passed():
    return packge_time.__call__()


def get_on_twenty(size, porta):
    com_name = porta.fisica.name

    response = porta.rx.getOnTime(size, 20)
    print(f'Utils response: {response}')
    
    if response == False:
        print("Não foi recebido uma resposta... Encerrando comunicação")
        mensagem_tipo_5 = Datagrama(5).createDatagrams()
        print(f'Enviando mensagem do tipo 5: {mensagem_tipo_5}')
        porta.sendData(mensagem_tipo_5)

        if com_name == 'COM1':
            write_client_log(create_log('send', mensagem_tipo_5[0], len(mensagem_tipo_5)))
        else:
            write_server_log(create_log('send', mensagem_tipo_5[0], len(mensagem_tipo_5)))

        porta.disable()
        sys.exit()
    
    elif response[0] == 5:
        if com_name == 'COM1':
            write_client_log(create_log('get', response[0], len(response)))
        else:
            write_server_log(create_log('get', response[0], len(response)))

        print('Mensagem do tipo Time Out recebida...')
        print('A comunicação será encerrada!')
        porta.disable()
        sys.exit()
    
    else:
        print(f'Comunicação reestabelecida com sucesso! Resposta enviada: {response}')
        return response


def get_on_time(size, porta):
    com_name = porta.fisica.name
    response = porta.rx.getOnTime(size, 5)

    if response == False:
        time.sleep(1)
        print('Inatividade percebida...')
        new_reponse = get_on_twenty(size, porta)
        return new_reponse

    elif response[0] == 5:
        if com_name == 'COM1':
            write_client_log(create_log('get', response[0], len(response)))
        else:
            write_server_log(create_log('get', response[0], len(response)))

        print('Mensagem do tipo Time Out recebida...')
        print('A comunicação será encerrada!')
        porta.disable()
        sys.exit()
    
    else:
        return response


def create_log(get_or_send, TYPE, size, ID=None, n_packages=None):
    # https://www.programiz.com/python-programming/datetime/current-datetime
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y/%H:%M:%S")

    if ID == None and n_packages == None:
        log = dt_string+'/'+get_or_send+'/'+str(TYPE)+'/'+str(size)

    elif ID != None and n_packages == None:
        log = dt_string+'/'+get_or_send+'/'+str(TYPE)+'/'+str(size)+'/'+str(ID)

    else:
        log = dt_string+'/'+get_or_send+'/'+str(TYPE)+'/'+str(size)+'/'+str(ID)+'/'+str(n_packages)

    return log


def write_client_log(log):
     with open("logs/Client5.txt", "a") as f:
        f.write(f"{log}\n")


def write_server_log(log):
    with open("logs/Server5.txt", "a") as f:
     f.write(f"{log}\n")