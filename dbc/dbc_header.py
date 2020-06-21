import bytes_util
from dataclasses import dataclass


@dataclass(init=False)
class DBCHeader():
    magic: str
    record_count: int
    field_count: int
    record_size: int
    string_block_size: int
    size: int

    def __init__(self, file):
        self.size = 4 * 5
        header_bytes = file.read(self.size)
        self.magic = header_bytes[0:4]
        self.record_count = bytes_util.bytes_util.to_int(header_bytes[4:8])
        self.field_count = bytes_util.to_int(header_bytes[8:12])
        self.record_size = bytes_util.to_int(header_bytes[12:16])
        self.string_block_size = bytes_util.to_int(header_bytes[16:20])

    def to_bytes(self):
        return [self.magic,
                bytes_util.to_bytes(self.record_count, 4),
                bytes_util.to_bytes(self.field_count, 4),
                bytes_util.to_bytes(self.record_size, 4),
                bytes_util.to_bytes(self.string_block_size, 4)]
