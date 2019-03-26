"""
Module contains class for result readings
"""
from typing import List, NamedTuple
from collections import namedtuple


class ReaderResult:
    """
    Class to store reading data inside
    """

    def __init__(self):
        self.container: List[NamedTuple] = []
        self.key_value_pair = namedtuple("Result", "key values")

    def add(self, key: str, *values: str) -> None:
        """
        Add key value pair to container

        Args:
            key(str): Key to identify values with
            *values(str): Values to add to key
        """
        data = self.key_value_pair(key=key, values=values)
        self.container.append(data)

    def add_list(self, key: str, values: List[str]) -> None:
        """
        Add key value pair to container

        Args:
            key(str): Key to identify values with
            values(list): Values to add to key
        """
        data: NamedTuple
        if values:
            data = self.key_value_pair(key=key, values=tuple(values))
        else:
            data = self.key_value_pair(key=key, values=(None))
        self.container.append(data)
