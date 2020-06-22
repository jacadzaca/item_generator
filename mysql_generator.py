def generate_preface(template_entry: int, first_entry: int):
    return 'DROP TABLE tmp;\n' \
        f'USE world;\n' \
        f'SET SQL_SAFE_UPDATES = 0;\n' \
        f'CREATE TEMPORARY TABLE tmp SELECT *' \
        f'FROM item_template WHERE entry = {template_entry};\n' \
        f'UPDATE tmp SET entry={first_entry - 1} ' \
        f'WHERE entry = {template_entry};\n'


def create_sql_insert(entry: int, last_entry: int):
    if last_entry > entry:
        raise ValueError('item.entry must be greater than the last_entry')
    return f'UPDATE tmp SET entry={entry} WHERE entry = {last_entry}; ' \
           f'INSERT INTO item_template SELECT * FROM tmp ' \
           f'WHERE entry = {entry};'


def generate_end():
    return 'DROP TABLE tmp;'
