from utils import *


class Test():
    def __init__(self, h0, h1=None):
        self.h1 = h1

    def get_h1(self):
        return self.h1


teste = Test(1, 3)
print(teste.get_h1())


print(isinstance(int_to_byte(1), bytes))

print(int.from_bytes(int_to_byte(2), byteorder='big'))