def int_to_byte(number):
    byte_number = (number).to_bytes(1, 'big')
    return byte_number


def byte_to_int(byte):
    number = int.from_bytes(byte, byteorder='big')
    return number