import dbc.bytes_util as bytes_util
from typing import BinaryIO
from dbc.dbc_header import DBCHeader


class RecordIterator():
    def __init__(self, file: BinaryIO, dbc_header: DBCHeader,
                 record_creator, field_size: int, size: int,
                 new_records=None):
        self._f = file
        self._header = dbc_header
        self._record_creator = record_creator
        self._field_size = field_size
        self._size = size
        self.new_records = new_records

    def __iter__(self):
        self._f.seek(self._header.size)
        return self

    def __next__(self):
        if self._f.tell() < self._size:
            return self._record_creator(*self._read_record())
        elif self.new_records:
            return next(self.new_records)
        else:
            raise StopIteration

    def _read_record(self):
        return [bytes_util.to_int(self._f.read(self._field_size))
                for _ in range(self._header.field_count)]

    """
    when using, keep in mind that @file_handler's
    position is being manged by this class
    @record_cretor is a function returing an instance
    of the record that should be returned during the iteration
    """
    @classmethod
    def create(cls, file_handler: BinaryIO,
               dbc_header: DBCHeader, record_creator):
        field_size = dbc_header.record_size // dbc_header.field_count
        size = dbc_header.record_count * dbc_header.record_size
        return cls(file_handler, dbc_header, record_creator, field_size, size)
