ruff .
black .
python -m pytest --cov-report=xml --cov-report=html --cov-report=lcov --cov=competencias -s $@
