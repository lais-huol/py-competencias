# Python Competencias

[![Coverage Status](https://coveralls.io/repos/github/lais-huol/py-competencias/badge.svg?branch=main)](https://coveralls.io/github/lais-huol/py-competencias?branch=main)

Implementação em Python de biblioteca para trabalhar com Competencias no estilo YYYYMM.

Retorna a lista de competêncais dada uma faixa de competências, a competência atual, a competência passada e a competência futura. Como atual entende-se o timestamp do now(). Cada competência tem os atributos as_int, as_decimal, as_date, as_datetime, as_time e as_string, conforme documentado abaixo.

## Como usar

```bash
pip install competencias
```

```python
from competencias import Competencia

# para a competência atual
Competencias.current

# para a próxima competência
Competencias.current.next

# para a competência anterior
Competencias.current.previous

# para a competência 202301
Competencias.get_instance(date(2023, 1, 25))

# para a competência 2022/12, partindo da competência 2023/01
Competencias.get_instance(date(2023, 1, 25)).previous

# para as competências entre 2022/01 e 2023/11
for c in Competencias.range(date(2022, 1, 1), date(2023, 11, 2)):
    print(c)

# para o ano da competência
Competencias.get_instance(date(2024, 2, 25)).date.year == 2024
Competencias.get_instance(date(2024, 2, 25)).year == 2024

# para o mês da competência
Competencias.get_instance(date(2024, 2, 25)).date.month == 2
Competencias.get_instance(date(2024, 2, 25)).month == 2

# para como uma inteiro 202301
Competencia.get_instance(date(2023, 1, 30)).as_int == 202301

# para como uma float 2023.01
Competencia.get_instance(date(2023, 1, 30)).as_float == 2023.01

# para como uma float (2023, 1)
Competencia.get_instance(date(2023, 1, 30)).as_tuple == (2023, 1)

# para o primeito dia da competência 2023/12
Competencia.get_instance(date(2023, 12, 25)).first_date == date(2023, 12, 1)

# para o último dia da competência 2023/12
Competencia.get_instance(date(2023, 12, 25)).last_date == date(2023, 12, 31)

# para o primeiro carimbo de tempo da competência 2023/12
Competencia.get_instance(date(2023, 12, 25)).first_datetime == datetime(2023, 12, 1, 0, 0, 0)

# para o último carimbo de tempo da competência 2023/12
Competencia.get_instance(date(2023, 12, 25)).last_datetime == datetime(2023, 12, 31, 23, 59, 59)

# para o primeiro carimbo de tempo da competência 2023/12
Competencia.get_instance(date(2023, 12, 25)).first_timestamp == 1701399600.0

# para o último carimbo de tempo da competência 2023/12
Competencia.get_instance(date(2023, 12, 25)).last_timestamp == 1704077999.0

# Para validar datas mínimas, todas linhas
class CompetenciaComMinimo(Competencia):
    MIN_DATE = date(2023, 11, 1)

# Agora todas as linhas abaixo vão lançar um exception
CompetenciaComMinimo.get_instance(date(2023, 12, 1))
CompetenciaComMinimo.get_instance(datetime(2023, 12, 1, 23, 59, 59))
CompetenciaComMinimo.get_instance(1800530519)
CompetenciaComMinimo.get_instance(1800530519.0)

class CompetenciaComMinimo(Competencia):
    MIN_DATE = date(2023, 11, 1)


# Agora todas as linhas abaixo vão lançar um exception
CompetenciaComMinimo.get_instance(date(2023, 12, 1))
CompetenciaComMinimo.get_instance(datetime(2023, 12, 1, 23, 59, 59))
CompetenciaComMinimo.get_instance(1800530519)
CompetenciaComMinimo.get_instance(1800530519.0)


```
