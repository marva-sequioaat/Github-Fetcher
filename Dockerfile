FROM python:3.11-slim

# Install pipx
RUN pip install --no-cache-dir pipx \
    && python3 -m pipx ensurepath

# Install Poetry using pipx and ensure it's in PATH
RUN python3 -m pipx install poetry \
    && python3 -m pipx ensurepath

# Add pipx binary directory to PATH
ENV PATH="/root/.local/bin:${PATH}"


WORKDIR /app

COPY cli-app-poetry ./
# /pyproject.toml cli-app-poetry/poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi 


RUN mkdir -p /data

ENTRYPOINT ["python","cli_app_poetry/main.py"]