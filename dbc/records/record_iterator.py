import bytes_util


class RecordIterator():
    def __init__(self, file, dbc_header, record_creator):
        self._f = file
        self._header = dbc_header
        self._record_creator = record_creator
        self._field_size = dbc_header.record_size // dbc_header.field_count
        self._size = self._header.record_count * self._header.record_size

    def __iter__(self):
        self._f.seek(self._header.size)
        return self

    def __next__(self):
        if self._f.tell() > self._size:
            raise StopIteration
        return self._record_creator(*self._read_record())

    def _read_record(self):
        return [bytes_util.to_int(self._f.read(self._field_size))
                for _ in range(self._header.field_count)]