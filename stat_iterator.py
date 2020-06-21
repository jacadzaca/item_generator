from statt import Stat
from stat_type import StatType


class StatIterator():
    def __init__(self, stat_type: StatType, min_value: int, max_value: int):
        self.stat_type = stat_type
        self.min_value = min_value
        self.max_value = max_value
        self._current = self.min_value - 1

    def __iter__(self):
        self._current = self.min_value - 1
        return self

    def __next__(self):
        if self._current < self.max_value:
            self._current += 1
            return Stat(self.stat_type, self._current)
        else:
            raise StopIteration

    def __repr__(self):
        return f'{self.stat_type} min:{self.min_value}, max:{self.max_value}'


def get_iterators(stats: dict) -> list:
    return [StatIterator(StatType[stat.upper()], stats[stat]['minValue'],
                         stats[stat]['maxValue']) for stat in stats.keys()]
