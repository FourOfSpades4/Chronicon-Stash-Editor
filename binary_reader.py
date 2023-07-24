import struct

def read_string(binary):
    cur = 0

    # Get String Length
    length = read_int(binary)
    cur += 8

    # Get String
    string = ""
    for _ in range(length):
        char = "".join([chr(binary[cur + i]) for i in range(2)])
        char = int.from_bytes(bytes.fromhex(char), byteorder="little")
        string += chr(char)
        cur += 2
    
    return string

def write_string(string):
    string = str(string)
    binary = write_int(len(string))
    for char in string:
        binary += bytes(hex(ord(char))[2:].upper(), encoding="ascii")
    
    return binary

def read_int(binary):
    integer = "".join([chr(binary[i]) for i in range(8)])
    integer = struct.unpack('<i', bytearray.fromhex(integer))[0]

    return integer

def write_int(i):
    i = int(i)
    integer = hex(struct.unpack('<i', struct.pack('<i', i))[0])[2:].upper()
    if len(integer) % 2 == 1:
        integer = "0" + integer
    for _ in range(8 - len(integer)):
        integer += "0"

    return bytes(integer, encoding="ascii")

def read_double(binary):
    double = "".join([chr(binary[i]) for i in range(16)])
    double = struct.unpack('<d', bytearray.fromhex(double))[0]

    return double

def write_double(i):
    i = float(i)
    double = hex(struct.unpack('>Q', struct.pack('<d', i))[0])[2:].upper()
    for _ in range(16 - len(double)):
        double = "0" + double

    return bytes(double, encoding="ascii")

def binary_to_string(binary):
    print(binary)
    for i in range(0, len(binary), 2):
        value = chr(binary[i]) + chr(binary[i + 1])
        print(str(value) + " ", end="")
    print()