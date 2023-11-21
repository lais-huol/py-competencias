docker build -t rds-core .

docker run -it --rm -v `pwd`:/app rds-core bash -c 'ruff .'

docker run --user 1000 -it --rm -v `pwd`:/app rds-core bash -c 'python -m pytest -s'
