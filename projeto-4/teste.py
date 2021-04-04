from utils2 import *

packge_time = TimedValue()

def have_passed():
    return packge_time.__call__()

pacote = 0
while True:
    print(have_passed())
