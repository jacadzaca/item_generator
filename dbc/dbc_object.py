import copy
import dbc.edit
from dbc_header import DBCHeader
from dbc.records.record_iterator import RecordIterator


class DBCObject():
    '''
    dbc_file MUST be opened in a rb+ mode
    '''

    def __init__(self, dbc_file):
        self._f = dbc_file
        self._header = DBCHeader(self._f)
        self._records = RecordIterator(self._f, self._header)
        self._template = None

    def set_template_record(self, entry):
        self._template = dbc.edit.find(entry, self._records)

    def add_record(self, entry, display_id):
        if self._template is None:
            raise ValueError(f'no template, {self}.set_template_record() ')
        template = copy.deepcopy(self._template)
        template.entry = entry
        template.display_id = display_id
        dbc.edit.append_record(template, self._header, self._f)
