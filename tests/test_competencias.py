import unittest
from datetime import date, datetime
from competencias import Competencia
from dateutil.zoneinfo import gettz


class TestCompetencias(unittest.TestCase):
    def __init__(self, method_nname: str = "runTest"):
        super().__init__(methodName=method_nname)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_validate_raising(self):
        with self.assertRaisesRegex(ValueError, "Deve ser.*None.*"):
            Competencia.validate(None)

    def test_validate_sem_minimo(self):
        class CompetenciaSemMinimo(Competencia):
            MIN_DATE = None
            MIN_DATETIME = None
            MIN_INT = None
            MIN_FLOAT = None

        self.assertEqual(CompetenciaSemMinimo.validate(date(2023, 11, 1)), date(2023, 11, 1))
        self.assertEqual(CompetenciaSemMinimo.validate(datetime(2023, 11, 1, 23, 59, 59)), date(2023, 11, 1))
        self.assertEqual(CompetenciaSemMinimo.validate(1700530519), date(2023, 11, 1))
        self.assertEqual(CompetenciaSemMinimo.validate(1700530519.0), date(2023, 11, 1))
        self.assertEqual(CompetenciaSemMinimo.validate("202311"), date(2023, 11, 1))

    def test_validate_com_minimo(self):
        class CompetenciaComMinimo(Competencia):
            MIN_DATE = date(2023, 11, 1)
            MIN_DATETIME = datetime(2023, 11, 1, 23, 59, 59)
            MIN_INT = 1700530519
            MIN_FLOAT = 1700530519.0

        self.assertEqual(CompetenciaComMinimo.validate(date(2023, 11, 1)), date(2023, 11, 1))
        self.assertEqual(CompetenciaComMinimo.validate(datetime(2023, 11, 1, 23, 59, 59)), date(2023, 11, 1))
        self.assertEqual(CompetenciaComMinimo.validate(1700530519), date(2023, 11, 1))
        self.assertEqual(CompetenciaComMinimo.validate(1700530519.0), date(2023, 11, 1))

    def test_validate_com_minimo_raising(self):
        class CompetenciaComMinimo(Competencia):
            MIN_DATE = date(2023, 12, 1)
            MIN_DATETIME = datetime(2023, 12, 1, 23, 59, 59)
            MIN_INT = 1703134797
            MIN_FLOAT = 1703134797.0

        with self.assertRaisesRegex(ValueError, ".*'datetime\.date'.*"):
            CompetenciaComMinimo.validate(date(2023, 11, 1))

        with self.assertRaisesRegex(ValueError, ".*'datetime\.datetime'.*"):
            CompetenciaComMinimo.validate(datetime(2023, 11, 1, 23, 59, 59))

        with self.assertRaisesRegex(ValueError, ".*'int'.*"):
            CompetenciaComMinimo.validate(1700530519)

        with self.assertRaisesRegex(ValueError, ".*'float'.*"):
            CompetenciaComMinimo.validate(1700530519.0)

        with self.assertRaisesRegex(ValueError, ".*'list'.*"):
            CompetenciaComMinimo.validate([])

        with self.assertRaisesRegex(ValueError, ".* None\."):
            CompetenciaComMinimo.validate(None)

    def test_init(self):
        self.assertIsInstance(Competencia(2023, 11), Competencia)
        self.assertEqual(Competencia(2023, 11).date, date(2023, 11, 1))

    def test_get_instance(self):
        self.assertIsInstance(Competencia.get_instance(1700530519.0), Competencia)
        self.assertEqual(Competencia.get_instance(date(2023, 11, 1)).date, date(2023, 11, 1))
        self.assertEqual(Competencia.get_instance(datetime(2023, 11, 1, 23, 59, 59)).date, date(2023, 11, 1))
        self.assertEqual(
            Competencia.get_instance(datetime(2023, 11, 1, 23, 59, 59, tzinfo=gettz("America/Fortaleza"))).date,
            date(2023, 11, 1),
        )
        self.assertEqual(Competencia.get_instance(1700530519).date, date(2023, 11, 1))
        self.assertEqual(Competencia.get_instance(1700530519.0).date, date(2023, 11, 1))

    def test_get_current(self):
        t = datetime.today()
        self.assertEqual(Competencia.get_current().date, date(t.year, t.month, 1))

    def test_range(self):
        self.assertEqual(len(Competencia.range(date(2022, 1, 1), date(2023, 11, 1))), 23)
        self.assertEqual(len(Competencia.range(date(2023, 1, 1), date(2022, 11, 1))), 0)

    def test_previous(self):
        p = Competencia.get_instance(date(2023, 11, 1)).previous
        self.assertIsInstance(p, Competencia)
        self.assertEqual(p.date, date(2023, 10, 1))

    def test_next(self):
        n = Competencia.get_instance(date(2023, 11, 1)).next
        self.assertIsInstance(n, Competencia)
        self.assertEqual(n.date, date(2023, 12, 1))

    def test_year(self):
        self.assertEqual(Competencia.get_instance(date(2023, 11, 1)).year, 2023)

    def test_month(self):
        self.assertEqual(Competencia.get_instance(date(2023, 11, 1)).month, 11)

    def test_as_int(self):
        self.assertEqual(Competencia.get_instance(date(2023, 1, 30)).as_int, 202301)

    def test_as_float(self):
        self.assertEqual(Competencia.get_instance(date(2023, 1, 30)).as_float, 2023.01)

    def test_as_tuple(self):
        self.assertEqual(Competencia.get_instance(date(2023, 1, 30)).as_tuple, (2023, 1))

    def test_first_date(self):
        self.assertEqual(Competencia.get_instance(date(2023, 12, 25)).first_date, date(2023, 12, 1))

    def test_last_date(self):
        self.assertEqual(Competencia.get_instance(date(2023, 12, 25)).last_date, date(2023, 12, 31))

    def test_first_datetime(self):
        self.assertEqual(Competencia.get_instance(date(2023, 12, 25)).first_datetime, datetime(2023, 12, 1, 0, 0, 0))

    def test_last_datetime(self):
        self.assertEqual(Competencia.get_instance(date(2023, 12, 25)).last_datetime, datetime(2023, 12, 31, 23, 59, 59))

    def test_first_timestamp(self):
        self.assertEqual(
            Competencia.get_instance(date(2023, 12, 25)).first_timestamp, datetime(2023, 12, 1, 0, 0, 0).timestamp()
        )

    def test_last_timestamp(self):
        self.assertEqual(
            Competencia.get_instance(date(2023, 12, 25)).last_timestamp, datetime(2023, 12, 31, 23, 59, 59).timestamp()
        )

    def test_str(self):
        self.assertEqual(Competencia.get_instance(date(2023, 12, 25)).__str__(), "2023/12")

    def test_mes_por_extenso(self):
        c = Competencia.get_instance(date(2023, 12, 25))
        self.assertEqual(c.mes_por_extenso, "Dezembro")
