import sys
from setuptools import setup, find_packages

version = "1.0.5"
if len(sys.argv) >= 3 and sys.argv[1] == "validate_tag":
    if sys.argv[2] != version:
        raise Exception(f"A versão TAG [{sys.argv[2]}] é diferente da versão no arquivo setup.py [{version}].")
    exit()


requirements = ["python-dateutil>=2.8.2"]
with open("requirements.txt", "w") as file1:
    for requirement in requirements:
        file1.write(f"{requirement}\n")

setup(
    **{
        "name": "competencias",
        "description": "Implementação em Python de biblioteca para trabalhar com Competencias no estilo YYYYMM.",
        "long_description": open("README.md").read(),
        "long_description_content_type": "text/markdown",
        "license": "Apache-2.0",
        "author": "Kelson da Costa Medeiros",
        "author_email": "kelson.medeiros@lais.huol.ufrn.br",
        "packages": find_packages(),
        "version": version,
        "download_url": f"https://github.com/lais-huol/py-competencias/releases/tag/{version}",
        "url": "https://github.com/lais-huol/py-competencias",
        "keywords": ["competencia"],
        "python_requires": ">=3.9",
        "install_requires": [
            "python-dateutil>=2.8.2",
        ],
        "classifiers": [
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    }
)
