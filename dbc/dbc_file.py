import copy
import dbc.edit
from dbc_header import DBCHeader
from dbc.records.record_iterator import RecordIterator


class DBCFile():
    '''
    file_descriptor MUST be opened in a rb+ mode
    '''

    def __init__(self, file_descriptor, template_entry):
        self._f = file_descriptor
        self._header = DBCHeader(self._f)
        self.records = RecordIterator(self._f, self._header)
        self._template = dbc.edit.find(template_entry, self.records)

    def add_record(self, entry, display_id):
        template = copy.deepcopy(self._template)
        template.entry = entry
        template.display_id = display_id
        dbc.edit.append_record(template, self._header, self._f)
