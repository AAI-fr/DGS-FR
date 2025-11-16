import struct
from io import BytesIO

class EndianBinaryWriter:
    def __init__(self,filepath : str, endianness : str = 'little'): #overwritten
        self.set_endianness(endianness)
        self.filepath = filepath
        self.file = open(self.filepath,mode='wb')
        self.write = self.file.write
        self.tell = self.file.tell
        self.seek = self.file.seek

    def set_endianness(self, endianness : str):
        if endianness == 'little':
            self.endian_flag = '<'
        elif endianness == 'big':
            self.endian_flag = '>'
        else:
            raise Exception(r"Unknown endianness : should be 'little' or 'big'")

    def write_Int8(self, value: int):
        self.write(struct.pack(f'{self.endian_flag}b', value))

    def write_UInt8(self, value: int):
        self.write(struct.pack(f'{self.endian_flag}B', value))

    def write_Int16(self, value: int):
        self.write(struct.pack(f'{self.endian_flag}h', value))
    
    def write_UInt16(self, value: int):
        self.write(struct.pack(f'{self.endian_flag}H', value))

    def write_Int32(self, value: int):
        self.write(struct.pack(f'{self.endian_flag}i', value))

    def write_UInt32(self, value: int):
        self.write(struct.pack(f'{self.endian_flag}I', value))

    def write_Int64(self, value: int):
        self.write(struct.pack(f'{self.endian_flag}q', value))

    def write_UInt64(self, value: int):
        self.write(struct.pack(f'{self.endian_flag}Q', value))

    def write_float32(self, value : float):
        self.write(struct.pack(f'{self.endian_flag}f', value))

    def write_string(self, string : str, encoding : str, null_terminator : bool = False):
        self.write(string.encode(encoding))
        if null_terminator: self.write('\x00'.encode(encoding))

    def pad(self, alignment: int):
        mod = self.tell() % alignment
        if mod != 0:
            self.write(bytes(alignment - mod))

class EndianBinaryFileWriter(EndianBinaryWriter):
    def __init__(self,filepath : str, endianness : str = 'little'):
        self.set_endianness(endianness)
        self.filepath = filepath
        self.file = open(self.filepath,mode='wb')
        self.write = self.file.write
        self.tell = self.file.tell
        self.seek = self.file.seek

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class EndianBinaryStreamWriter(EndianBinaryWriter):
    def __init__(self, endianness : str = 'little'):
        self.set_endianness(endianness)
        self.stream = BytesIO()
        self.write = self.stream.write
        self.tell = self.stream.tell
        self.seek = self.stream.seek
        self.getvalue = self.stream.getvalue