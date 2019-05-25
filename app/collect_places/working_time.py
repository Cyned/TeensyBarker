import re

from typing import Sequence, Optional


class WorkingTime(object):

    # encoder dict
    weekdays = {
        'monday':    '1',
        'tuesday':   '2',
        'wednesday': '3',
        'thursday':  '4',
        'friday':    '5',
        'saturday':  '6',
        'sunday':    '7',
    }

    def __init__(self):
        self._days   = None
        self._time   = None
        self._ids    = None
        self.decoder = None

    def parse(self, ids: Sequence[str], times: Sequence[str]):
        """
        Parse working time.
        :param ids: ids of the place
        :param times: list of the working times
        """
        self._days = []
        self._time = []
        self._ids  = []
        for id_, time in zip(ids, times):
            days = dict()
            for t in time:
                tmp = re.match(r'^(?P<weekday>[a-z]*):(?P<working_time>.*)', self.clean_time(t))
                if days.get(tmp.group('working_time')):
                    days[tmp.group('working_time')] += self.weekdays[tmp.group('weekday')]
                else:
                    days[tmp.group('working_time')] = self.weekdays[tmp.group('weekday')]
            self._ids.extend([id_] * len(days))
            self._time.extend(days.keys())
            self._days.extend(days.values())

    def decode(self, days: Optional[str], time: str) -> dict:
        """
        Decode working time encoded in {integer: working_time, } to {weekday: working_time, }
        :param days: number of weekdays (example: 125 - Monday, Thursday, Friday)
        :param time: working time
        :return: dictionary, {weekday: working_time, }
        """
        working_time = dict()
        if type(days) is int:
            days = str(days)
        for day in days:
            weekday = get_key(self.weekdays, day)
            if weekday:
                working_time[weekday] = time

        return working_time

    @staticmethod
    def clean_time(query: str) -> str:
        """
        Lower and clean string
        :param query: query to clean
        :return: cleaned string
        """
        return query.lower().replace(' ', '')

    @property
    def days(self):
        return self._days

    @property
    def time(self):
        return self._time

    @property
    def ids(self):
        return self._ids


def get_key(dict_: dict, value: str) -> Optional[str]:
    """
    Search key of the dictionary via its value
    :param dict_: dictionary to parse
    :param value: value to search
    :return: key
    """
    for k, v in dict_.items():
        if v == value:
            return k
    return None
