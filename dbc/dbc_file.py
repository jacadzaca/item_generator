import copy
import dbc.edit
from dbc_header import DBCHeader
from dbc.records.record_iterator import RecordIterator


class DBCFile():
    '''
    file_descriptor MUST be opened in a rb+ mode
    '''

    def __init__(self, file_handle, header, records, template_entry):
        self._f = file_handle
        self._header = header
        self.records = records
        self._template = dbc.edit.find(template_entry, self.records)

    def add_record(self, entry, display_id):
        template = copy.deepcopy(self._template)
        template.entry = entry
        template.display_id = display_id
        dbc.edit.append_record(template, self._header, self._f)

    @classmethod
    def from_file_handle(cls, file_handle, record_creator, template_entry):
        header = DBCHeader(file_handle)
        records = RecordIterator(file_handle, header, record_creator)
        template = dbc.edit.find(template_entry, records)
        return cls(file_handle, header, records, template)
