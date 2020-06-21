import collections


Stat = collections.namedtuple('Stat', 'stat_type value')


def stat_to_sql(stat_count, stat: Stat) -> str:
    count = stat_count.__next__()
    return f'stat_type{count}={stat.stat_type.value}, '\
           f'stat_value{count}={stat.value}'
