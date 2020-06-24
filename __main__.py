#!/usr/bin/python3
import sys
import json
import random
import itertools
import functools
import stat_iterator
import mysql_generator
from item import Item
from dbc.dbc_file import DBCFile
from dbc.records.item_record import ItemRecord


def _create_item(name, display_ids, stats, entry):
    return Item(name, entry, random.choice(display_ids), stats)


def main():
    usage = 'usage: item-creator item_definition.json' \
            '[sql_file] [Item.dbc path]'
    default_sql = 'generated/random-items.sql'
    default_item_dbc = 'generated/Item.dbc'
    if (len(sys.argv) < 2):
        print(usage)
        sys.exit(-1)
    item_definition = sys.argv[1]
    sql_file = sys.argv[2] if 2 < len(sys.argv) else default_sql
    item_dbc = sys.argv[3] if 3 < len(sys.argv) else default_item_dbc

    try:
        with open(item_definition) as f:
            config = json.loads(f.read())
            display_ids = config['displayIds']
            first_entry = config['firstEntry']
            template_entry = config['templateEntry']

        dbc_f = open(item_dbc, 'rb+')
        sql_f = open(sql_file, 'w')
    except OSError as e:
        print(e)
        sys.exit(-1)
    except KeyError as e:
        print(f'{item_definition} is missing key: {e}')
        sys.exit(-1)
    else:
        stats = stat_iterator.get_iterators(config['stats'])
        item_creator = functools.partial(_create_item,
                                         config['name'],
                                         display_ids)
        stats_entry_zip = zip(itertools.product(*stats),
                              itertools.count(first_entry))
        items = itertools.starmap(item_creator, stats_entry_zip)
        with dbc_f, sql_f:
            dbc_file = DBCFile.from_file_handle(dbc_f,
                                                ItemRecord,
                                                template_entry)
            sql_f.write(mysql_generator.generate_preface(
                template_entry, first_entry))
            for item in items:
                dbc_file.add_record(item.entry, item.display_id)
                sql_f.write(mysql_generator.create_sql_insert(
                    item.entry, item.entry - 1) + '\n')
                sql_f.write(item.to_sql() + '\n')
            sql_f.write(mysql_generator.generate_end() + '\n')


if __name__ == '__main__':
    main()
