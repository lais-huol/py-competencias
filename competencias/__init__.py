# -*- coding: utf-8 -*-
from typing import List, Optional, Union, TypeVar, Any
from datetime import date, datetime, timezone
import calendar
from dateutil.rrule import rrule, MONTHLY
from dateutil.relativedelta import relativedelta


Competencia = TypeVar("Competencia", bound="Competencia")


class Competencia(object):
    MIN_DATE = date(1970, 1, 1)
    TIMEZONE = timezone.utc
    MESES = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    __instances = {}

    def __init__(self, year: int, month: int):
        """Never create a Competencia directly, allways use get_instance.

        Args:
            year (int): a valid year
            month (int): a valid month
        """
        self.date = date(year, month, 1)

    def __str__(self):
        return f"{self.as_int}"

    @classmethod
    def _validate(cls, value: date, datetype: Any) -> date:
        if cls.MIN_DATE is not None and value < cls.MIN_DATE:
            raise ValueError(f"Para {datetype} a menor data é {cls.MIN_DATE}, mas você informou {value}.")
        return value

    @classmethod
    def validate(cls, value: Union[int, date, datetime, float, str]) -> date:
        if value is None:
            raise ValueError("Deve ser informada alguma date, mas você informou None.")

        if type(value) not in [int, date, datetime, float, str]:
            raise ValueError(
                f"Deve ser informado um date, datetime, int, float ou str (AAAAMM), mas você informou {type(value)}={value}."
            )

        if isinstance(value, datetime) or isinstance(value, date):
            return cls._validate(date(value.year, value.month, 1), value.__class__)

        if isinstance(value, int) or isinstance(value, float):
            return cls._validate(datetime.fromtimestamp(value).date().replace(day=1), value.__class__)

        if isinstance(value, str):
            return cls._validate(date(int(value[0:4]), int(value[4:6]), 1), value.__class__)

    @classmethod
    def get_instance(cls, value: Union[date, datetime, int, float, str]) -> Competencia:
        _date = cls.validate(value)
        if _date not in cls.__instances:
            cls.__instances[_date] = cls(_date.year, _date.month)
        return cls.__instances[_date]

    @classmethod
    def range(cls, start: Optional[Competencia] = None, end: Optional[Competencia] = None) -> List[Competencia]:
        dtstart = start.first_date if start is not None else cls.MIN_DATE
        until = end.first_date if end is not None else date.today()
        return [cls.get_instance(dt) for dt in rrule(MONTHLY, dtstart=dtstart, until=until)]

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
    def as_tuple(self) -> tuple:
        return (self.year, self.month)

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

    @property
    def first_timestamp(self) -> float:
        "Return POSIX timestamp as float"
        return self.first_datetime.timestamp()

    @property
    def last_timestamp(self) -> float:
        "Return POSIX timestamp as float"
        return self.last_datetime.timestamp()

    @property
    def mes_por_extenso(self):
        return self.__class__.MESES.get(self.date.month, "-")
