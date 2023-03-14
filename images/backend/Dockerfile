FROM python:3.10 as dev

ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# Install poetry
RUN pip install --upgrade pip && \
    pip install pipx && \
    pipx install git+https://github.com/adriangb/poetry@skip-path-dep-install && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
COPY packages/api/pyproject.toml packages/api/

RUN poetry install --no-directory

COPY packages packages

RUN poetry install

FROM dev as build

RUN cd packages/api && poetry build

FROM python:3.10-slim as prod

COPY --from=build /app/packages/api/dist/*.whl /dist/

RUN pip install /dist/*.whl