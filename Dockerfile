FROM python:3.8-bullseye

ADD requirements.txt /
ADD requirements-dev.txt /

# Requirements
RUN pip install --upgrade pip \
    && pip install -r requirements.txt -r requirements-dev.txt \
    && RELEASE_VERSION=$(grep version setup.py | awk -F\" '{print $2}') \
    && echo $RELEASE_VERSION

WORKDIR /app

# # Static type check
# RUN mypy --warn-unused-configs --python-version 3.8 --show-error-context --show-column-numbers --show-error-end --show-error-codes --pretty --html-report artifacts/statictypecheck --cobertura-xml-report statictypecheck rds_core

# # Static type check
# RUN python -m pytest

# # Build package
# RUN python setup.py sdist \
#     && python setup.py validate_tag $RELEASE_VERSION && python setup.py sdist

# Deploy to PyPi
# uses: pypa/gh-action-pypi-publish@v1.8.5
# with:
# user: __token__
# password: ${{ secrets.PYPI_API_TOKEN }}
