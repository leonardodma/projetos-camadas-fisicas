"""
------------------------------------------------
Extrutua do Head:

h0 = Tipo mensagem
h1 = id cliente
h2 = id servidor
h3 = número total de pacotes
h4 = número do pacote sendo enviado
h5 = se for handshake -> id do arquivo
         se for dados -> tamanho do paylaod
h6 = pacote solicitado para recomeço de envio
h7 = último pacote recebido com sucesso
h8 e h9 = CRC

Tipo 1: Handshake
Tipo 2: Servidor responde Handshake
Tipo 3: Envio de dados
------------------------------------------------
"""
# Realizando imports necessários:
from math import ceil
from utils import *

# Declarando variáveis em bytes:
eop = (4294967295).to_bytes(4, byteorder='big')

zero_byte = (0).to_bytes(1, 'big')
one_byte = (1).to_bytes(1, 'big')
two_byte = (2).to_bytes(1, 'big')
client_id = one_byte
server_id = two_byte


class Head():
    def __init__(self, h0): # São fixos
        
        # Obrigatórios na inicialização
        self.h0 = int_to_byte(h0)

        # Dependem do tipo da Mensagem
        self.h3 = zero_byte
        self.h4 = zero_byte
        self.h5 = zero_byte
        self.h6 = zero_byte
        self.h7 = zero_byte

        # Fixos no projeto 4
        self.h1 = client_id
        self.h2 = server_id
        self.h8 = zero_byte
        self.h9 = zero_byte

    def messegeType(self):
        return byte_to_int(self.h0)
    
    def createHead(self):
        return self.h0 + self.h1 + self.h2 + self.h3 + self.h4 + self.h5 + self.h6 + self.h7 + self.h8 + self.h9
        

class Datagrama(Head):
    # Criar um datagrama -> Argumentos h0, Mensagem Facultativa
    def __init__(self, h0, joker=None):
        super().__init__(h0)

        if joker == None:
            self.id = None
            self.message = None
        else:
            if isinstance(joker, int):
                self.id = joker
                self.message = None
            else:
                self.id = None
                self.message = joker
         
    def createDatagrams(self):
        if self.message != None:
            number_of_packages = ceil(len(self.message)/114) # ceil = arredondar para cima
            self.h3 = int_to_byte(number_of_packages)


            if self.messegeType() == 3:
                datagrams = []

                ID = 1 # Primeiro pacote terá o ID = 1

                for i in range(0, len(self.message), 114):
                    if len(self.message) - i >= 114:
                        payload = self.message[0+i : 114+i]
                        payload_size_byte = int_to_byte(len(payload))
                        self.h5 = payload_size_byte
                        print(f'O tamanho do Payload do datagrama {ID} é: {len(payload)}')


                    else:
                        payload = self.message[i:]
                        print(f'O tamanho do último Payload (Datagrama {ID}) é: {len(payload)}')
                        payload_size_byte = int_to_byte(len(payload))
                        self.h5 = payload_size_byte
                    
                    self.h4 = int_to_byte(ID)

                    datagram = self.createHead() + payload + eop
                    datagrams.append(datagram)

                    print(f"Datagrama {ID}: {datagram}\n")

                    ID += 1

                return datagrams
            
            else:
                print('Handshake!')
                print(self.createHead())
                return self.createHead() + eop
        
        else:
            if self.messegeType() == 4:
                print(f'Pacote recebido com sucesso: {self.id}')
                self.h7 = int_to_byte(self.id)
                return self.createHead() + eop
            
            elif self.messegeType() == 6:
                print(f'Pacote para reenvio: {self.id}')
                self.h6 = int_to_byte(self.id)
                return self.createHead() + eop
            
            else:
                return self.createHead() + eop