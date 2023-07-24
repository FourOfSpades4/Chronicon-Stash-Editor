import codecs
import struct
from binary_reader import *

class Stat(object):
    def __init__(self, binary):
        self.name = None
        self.type = None
        self.value = None

        if binary is not None:
            self.read(binary)

    def __str__(self):
        return str(self.value)

    def read(self, binary):
        self.length = 0

        # Get Property Name
        
        self.name = read_string(binary[self.length:])
        self.length += 8 + len(self.name) * 2
        
        # Get Data Type
        self.type = read_int(binary[self.length:])
        self.length += 8

        # Get Double
        if self.type == 0:
            self.value = read_double(binary[self.length:])
            self.length += 16

        # Get String
        elif self.type == 1:
            self.value = read_string(binary[self.length:])
            self.length += 8 + len(self.value) * 2

        # Unknown Type
        else:
            self.length += 16

        # Skip Unknown Bytes
        self.unknown = binary[self.length:self.length+8]
        self.length += 8

    def write(self):
        binary = write_string(self.name)
        binary += write_int(self.type)
        
        if self.type == 0:
            binary += write_double(self.value)
        if self.type == 1:
            binary += write_string(self.value)
        
        binary += self.unknown

        return binary

    def set_value(self, value):
        self.value = value


class Item(object):
    def __init__(self, binary, unknown=False):
        self.stats = []

        if not unknown:
            self.read(binary)
        else:
            self.unknown = [binary]

    def __str__(self):
        string = ""
        string += self.get_name() + "\n"

        for stat in self.stats:
            if stat.name != "name":
                string += stat.name + ": " + str(stat.value) + "\n"
        
        return string

    def read(self, binary):
        self.length = 0
        self.unknown = []

        # Skip Unknown Bytes
        self.unknown.append(binary[self.length:self.length+8])
        self.length += 8

        # Get Number of Entries
        self.entries = read_int(binary[self.length:])
        self.length += 8
        
        # Skip Unknown Bytes
        self.unknown.append(binary[self.length:self.length+8])
        self.length += 8
        
        for _ in range(self.entries):
            stat = Stat(binary[self.length:])
            self.length += stat.length
            self.stats.append(stat)
            
        # Skip Unknown Bytes
        self.unknown.append(binary[self.length:self.length+12])
        self.length += 12

    def write(self):
        if len(self.unknown) > 1:
            binary = self.unknown[0]
            binary += write_int(self.entries)
            binary += self.unknown[1]
            for stat in self.stats:
                binary += stat.write()
            binary += self.unknown[2]
        else:
            binary = self.unknown[0]

        return binary

    def get_name(self):
        name = [s.value for s in self.stats if s.name == "name"]
        return name[0] if name else None

    def get_stat(self, name):
        for stat in self.stats:
            if stat.name == name:
                return stat
        return None

    def change_stat(self, name, value):
        for stat in self.stats:
            if stat.name == name:
                stat.value = value
                return True
        return False


class Stash(object):
    encoding = "ascii"

    def __init__(self, f=None):
        self.version = None
        self.size = None
        self.items = []
        self.file = f

        if f is not None:
            with open(f, 'r') as f:
                self.orig = f.read()
                data = self.orig.split(":")
                self.size = int(data[1][1:-7])
                self.version = data[4][2:-3]
                self.read(data[2][2:-8])

    def read(self, string):
        binary = codecs.decode(string, "hex")

        self.length = 20
        self.unknown = binary[0:self.length]
        while len(binary[self.length:]) > 0:
            if binary[self.length] == 0:
                self.items.append(Item(binary[self.length:self.length+20], 
                    unknown=True))
                self.length += 20
                continue
            else:
                item = Item(binary[self.length:])
                self.items.append(item)
                self.length += item.length

    def write(self):
        binary = self.unknown
        for item in self.items:
            binary += item.write()

        return codecs.encode(binary, "hex").decode(Stash.encoding).upper()

    def write_to_file(self, f):
        stash = self.orig.replace(self.orig.split(":")[2][2:-8], self.write())

        with open(f, 'w') as f:
            f.write(stash)
        
    def change_stat(self, item_name, stat_name, value):
        for item in self.items:
            if item.get_name() == item_name:
                return item.change_stat(stat_name, value)
        return False

    def get_item(self, item_name):
        for item in self.items:
            if item.get_name() == item_name:
                return item
        return None