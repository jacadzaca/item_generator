import copy
import dbc.edit
from dbc.dbc_header import DBCHeader
from dbc.records.record_iterator import RecordIterator

"""
Exposes a set of methods for manipulating a DBCFile,
to acquire a iterator of dbc_records use dbc_file.records
@see https://wowdev.wiki/DBC
"""


class DBCFile():
    """
   @file_handle MUST have read permissions (e.g rb)
   @file_handle is expected to be opened in binary mode
    """

    def __init__(self, file_handle, header: DBCHeader,
                 records: iter, template_entry: int):
        self._f = file_handle
        self._header = header
        self.records = records
        self._template = dbc.edit.find(template_entry, self.records)

    """
    in order for this method to work, the passed @file_handle
    MUST have write permissions (e.g rb+)
    this method changes the file's position
    """

    def add_record(self, entry, display_id):
        template = copy.deepcopy(self._template)
        template.entry = entry
        template.display_id = display_id
        dbc.edit.append_record(template, self._header, self._f)

    """
    this function changes the @file_handle's position.
    @file_handle MUST have AT LEAST read permissions (e.g rb)
    @file_handle is expected to be opened in binary mode
    for @record_creator @see dbc/records/record_iterator.py
    """
    @classmethod
    def from_file_handle(cls, file_handle, record_creator, template_entry):
        header = DBCHeader.from_file_handle(file_handle)
        records = RecordIterator.create(file_handle, header, record_creator)
        template = dbc.edit.find(template_entry, records)
        return cls(file_handle, header, records, template)
