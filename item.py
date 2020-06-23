import functools
import itertools
import statt
from dataclasses import dataclass


@dataclass
class Item():
    def to_sql(self) -> str:
        return f'UPDATE item_template SET ' \
               f'StatsCount={len(self.stats)}, ' \
               f'{self.create_sql_stats_update()}, ' \
               f'name="{self.name}", ' \
               f'displayid={self.display_id} ' \
               f'WHERE entry = {self.entry};'

    def create_sql_stats_update(self) -> str:
        helper = functools.partial(statt.stat_to_sql, itertools.count(1))
        return ', '.join(map(helper, self.stats))

    def __repr__(self):
        return f'item: {self.entry} ' \
               f'{self.name}, ' \
               f'{self.display_id}, ' \
               f'{self.stats}'
