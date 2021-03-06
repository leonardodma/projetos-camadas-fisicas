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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM2"                  # Windows(variacao de)



def main():
    try:
        com2 = enlace(serialName)
        com2.enable()

        print('A comunicação foi aberta com sucesso!')
        print('A recepção vai começar')
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      

        #acesso aos bytes recebidos
        print("Recebendo o tamanho da imagem...")
        size_img_bytes, n_sib = com2.getData(3) # 3 = quantidade de bytes para reservar     

        print("Tamanho recebido: {}".format(size_img_bytes))

        int_size = int.from_bytes(size_img_bytes, byteorder='big')
        print(int_size)

        rxBuffer, Rxlen = com2.getData(int_size)

    
        com2.sendData(Rxlen.to_bytes(3, byteorder='big'))


        print("recebeu imagem, tamanho: {}" .format(len(rxBuffer)))

        print('Salvando dados dos arquivos: ')

        imageW = './img/recebidaCopia.jpg'
        f = open(imageW, 'wb')
        f.write(rxBuffer)
            
    
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
