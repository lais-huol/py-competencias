docker build -t py-competencias .

docker run -it --rm -v `pwd`:/app py-competencias bash -c 'ruff check .'

docker run -it --rm -v `pwd`:/app py-competencias bash -c 'black .'

docker run --user 1000 -it --rm -v `pwd`:/app py-competencias -c 'python -m pytest -s'
