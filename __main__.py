#!/usr/bin/env python3
import argparse
import pathlib
import copy
import random
import itertools
import collections
import shutil

import yaml

from jinja2 import Environment, FileSystemLoader

from dbcpy.dbc_file import DBCFile
from dbcpy.records.item_record import ItemRecord

ItemDefinition = collections.namedtuple('ItemDefinition', 'name first_entry template_entry display_ids attributes')
Attribute = collections.namedtuple('Attribute', 'id value')
Item = collections.namedtuple('Item', 'name entry display_id attributes')

def to_attribute_id(attribute_name):
    """
    https://trinitycore.atlassian.net/wiki/spaces/tc/pages/2130222/item+template#item_template-stat_type
    """
    return {
        'mana': 0,
        'health': 1,
        'agility': 3,
        'strength': 4,
        'intellect': 5,
        'spirit': 6,
        'stamina': 7,
        'defense skill rating': 12,
        'dodge rating': 13,
        'parry rating': 14,
        'block rating': 15,
        'hit melee rating': 16,
        'hit ranged rating': 17,
        'hit spell rating': 18,
        'crit melee rating': 19,
        'crit ranged rating': 20,
        'crit spell rating': 21,
        'hit taken melee rating': 22,
        'hit taken ranged rating': 23,
        'hit taken spell rating': 24,
        'crit taken melee rating': 25,
        'crit taken ranged rating': 26,
        'crit taken spell rating': 27,
        'haste melee rating': 28,
        'haste ranged rating': 29,
        'haste spell rating': 30,
        'hit rating': 31,
        'crit rating': 32,
        'hit taken rating': 33,
        'crit taken rating': 34,
        'resilience rating': 35,
        'haste rating': 36,
        'expertise rating': 37,
        'attack power': 38,
        'ranged attack power': 39,
        'spell healing done': 41,
        'spell damage done': 42,
        'mana regeneration': 43,
        'armor penetration rating': 44,
        'spell power': 45,
        'health regen': 46,
        'spell penetration': 47,
        'block': 48,
    }[attribute_name]

def to_item_record(item, tempate_record):
    record = copy.copy(tempate_record)
    record.entry = item.entry
    record.display_id = item.display_id
    return record

def main():
    parser = argparse.ArgumentParser(description="a small script that outputs both DBC and SQL files need to create 'random' items",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('item_definition', help='the path to the YAML file containing description of items to be generated', type=pathlib.Path)
    parser.add_argument('--dbc_input', help='where the Item.dbc is located', default='Item.dbc', type=pathlib.Path)
    parser.add_argument('--dbc_output', help='where to output Item.dbc with new items', default='Item.dbc.gen', type=pathlib.Path)
    parser.add_argument('--sql_output', help='where to output the SQL with new items', default='items.sql', type=pathlib.Path)

    argv = parser.parse_args()

    with open(argv.item_definition) as f:
        raw = yaml.safe_load(f.read())
        raw['attributes'] = {raw_range['name']:range(raw_range['min'], raw_range['max'] + 1) for raw_range in raw['attributes']}
        item_definition = ItemDefinition(**raw)

    attributes_combinations = itertools.product(*item_definition.attributes.values())
    attributes_ids = map(to_attribute_id, item_definition.attributes.keys())
    attributes = (zip(attributes_ids, attributes_combination) for attributes_combination in attributes_combinations)
    attributes = (itertools.starmap(Attribute, attributes) for attribute in attributes)
    items = [Item(item_definition.name, entry, random.choice(item_definition.display_ids), attributes)
             for (entry, attributes) in enumerate(attributes, item_definition.first_entry)]

    sql = Environment(
        loader=FileSystemLoader('.'),
        trim_blocks=True,
        lstrip_blocks=True) \
    .get_template('items.jinja.sql') \
    .render(items=items, first_entry=item_definition.first_entry,
            attribute_count=len(item_definition.attributes),
            template_entry=item_definition.template_entry, enumerate=enumerate)

    with open(argv.sql_output, 'w') as sql_f:
        sql_f.write(sql)

    shutil.copyfile(argv.dbc_input, argv.dbc_output)
    with open(argv.dbc_output, 'r+b') as f:
        dbc_file = DBCFile.from_file(f, ItemRecord)
        template = dbc_file.records.find(item_definition.template_entry)
        dbc_file.records.append(*[to_item_record(item, template) for item in items])

if __name__ == '__main__':
    main()

