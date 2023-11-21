# -*- coding: utf-8 -*-
from typing import List, Optional, Union, TypeVar
from datetime import date, datetime
import calendar
from dateutil.rrule import rrule, MONTHLY
from dateutil.relativedelta import relativedelta


Competencia = TypeVar("Competencia", bound="Competencia")


class Competencia(object):
    FIRST_MOMENT = dict(day=1, hour=0, minute=0, second=0)
    MIN_DATE = None
    MIN_DATETIME = None
    MIN_INT = None
    MIN_FLOAT = None
    __instances = {}

    def __init__(self, year: int, month: int):
        """Never create a Competencia directly, allways use get_instance.

        Args:
            year (int): a valid year
            month (int): a valid month
        """
        self.date = date(year, month, 1)

    def __str__(self):
        return f"{self.date.year}{self.date.month}"

    @classmethod
    def validate(
        cls, value: Union[int, date, datetime, float]
    ) -> Union[date, datetime]:
        if type(value) not in [int, date, datetime, float]:
            raise ValueError(
                f"Deve ser informado um date, datetime, int ou float, mas você informou {type(value)}={value}."
            )

        def __validate(minvalue):
            if minvalue is not None and value < minvalue:
                raise ValueError(
                    f"Para {type(value)} a menor data é {minvalue}, mas você informou {value}."
                )
            return True

        if isinstance(value, datetime) and __validate(cls.MIN_DATETIME):
            return date(value.year, value.month, 1)

        if isinstance(value, date) and __validate(cls.MIN_DATE):
            return date(value.year, value.month, 1)

        if isinstance(value, int) and __validate(cls.MIN_INT):
            _value = datetime.fromtimestamp(value)
            return date(_value.year, _value.month, 1)

        if isinstance(value, float) and __validate(cls.MIN_FLOAT):
            _value = datetime.fromtimestamp(int(value))
            return date(_value.year, _value.month, 1)

    @classmethod
    def get_instance(cls, value: Union[date, datetime, int, float]) -> Competencia:
        _date = cls.validate(value)
        if _date not in cls.__instances:
            cls.__instances[_date] = Competencia(_date.year, _date.month)
        return cls.__instances[_date]

    @classmethod
    def range(
        cls,
        start: Optional[Union[date, datetime, int, float]] = None,
        end: Optional[Union[date, datetime, int, float]] = None,
    ) -> List[Competencia]:
        dtstart = cls.validate(start or datetime.now())
        until = cls.validate(end or datetime.now())
        return [
            cls.get_instance(dt) for dt in rrule(MONTHLY, dtstart=dtstart, until=until)
        ]

    @classmethod
    @property
    def current(cls) -> Competencia:
        return cls.get_instance(datetime.today())

    @property
    def previous(self) -> Competencia:
        return self.get_instance(self.date + relativedelta(months=-1))

    @property
    def next(self) -> Competencia:
        return self.get_instance(self.date + relativedelta(months=1))

    @property
    def year(self) -> int:
        return self.date.year

    @property
    def month(self) -> int:
        return self.date.month

    @property
    def as_int(self) -> int:
        return self.year * 100 + self.month

    @property
    def as_float(self) -> float:
        return float(self.year) + (float(self.month) / 100)

    @property
    def first_date(self) -> date:
        return date(self.date.year, self.date.month, 1)

    @property
    def last_date(self) -> date:
        return date(
            self.date.year,
            self.date.month,
            calendar.monthrange(self.date.year, self.date.month)[1],
        )

    @property
    def first_datetime(self) -> datetime:
        return datetime(self.date.year, self.date.month, 1)

    @property
    def last_datetime(self) -> datetime:
        last_day = calendar.monthrange(self.date.year, self.date.month)[1]
        return datetime(self.date.year, self.date.month, last_day, 23, 59, 59)
