FROM python:3.10 as dev

ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# Install poetry
RUN pip install --upgrade pip && \
    pip install pipx && \
    pipx install git+https://github.com/adriangb/poetry@skip-path-dep-install

COPY pyproject.toml poetry.lock ./
COPY packages/api/pyproject.toml packages/api/

RUN poetry install --no-directory

COPY packages/api packages/api
COPY noxfile.py ./

RUN poetry install

ENTRYPOINT [ "poetry", "run" ]

FROM dev as build

RUN cd packages/api && poetry build

FROM python:3.10-slim as prod

COPY --from=build /app/packages/api/dist/*.whl /dist/

RUN pip install /dist/*.whl