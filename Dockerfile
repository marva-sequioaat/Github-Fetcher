FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy and install the wheel package
COPY cli-app-poetry/dist/cli_app_poetry-0.1.0-py3-none-any.whl /tmp/

# Install the wheel file
RUN pip install /tmp/cli_app_poetry-0.1.0-py3-none-any.whl


# Install pytest and other dependencies needed for testing
RUN pip install pytest pytest-mock

# Copy only the test files
COPY tests /app/tests

# Create a persistent data directory
RUN mkdir -p /data

# Define the default command for the container
CMD [ "cli-app-poetry" ]

