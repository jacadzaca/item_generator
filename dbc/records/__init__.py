"""
stores different representations of dbc file structures
ALL representations should specify a strings method
that returns string to be put in string_block section,
if no strings are to be put, the implementation should return NO_STRING.
for different types of records @see https://wowdev.wiki/Category:DBC_WotLK
"""

NO_STRING = ['\0']
