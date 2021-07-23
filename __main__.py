#!/usr/bin/env python3
import argparse
import pathlib
import yaml
import random
import itertools
import collections
from dbc.dbc_file import DBCFile
from dbc.records.item_record import ItemRecord

ItemDefinition = collections.namedtuple('ItemDefinition', 'name first_entry template_entry display_ids attributes')
Attribute = collections.namedtuple('Attribute', 'attribute_id value')
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
    }[attribute_name]

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('item_definition', type=pathlib.Path)
    parser.add_argument('--dbc_output', default='Items.dbc.gen', type=pathlib.Path)
    parser.add_argument('--sql_output', default='items.sql', type=pathlib.Path)

    argv = parser.parse_args()

    with open(argv.item_definition) as f:
        raw = yaml.safe_load(f.read())
        raw['attributes'] = {raw_range['name']:range(raw_range['min'], raw_range['max'] + 1) for raw_range in raw['attributes']}
        item_definition = ItemDefinition(**raw)

    items = itertools.product(*item_definition.attributes.values())
    items = map(lambda values: zip(map(to_attribute_id, item_definition.attributes.keys()), values), items)
    items = map(lambda attributes: itertools.starmap(Attribute, attributes), items)
    items = [Item(item_definition.name, entry, random.choice(item_definition.display_ids), attributes) for (entry, attributes) in zip(itertools.count(start=item_definition.first_entry), items)]

    print(*items, sep='\n')

    print(item_definition)


if __name__ == '__main__':
    main()

