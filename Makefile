# Makefile for the Python application

# Variables
IMAGE_NAME = cli-app


# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the application
run:
# Validate that CONFIG_PATH is provided
ifndef CONFIG_PATH
	$(error CONFIG_PATH is not set. Please provide the path to the config file.)
endif
	docker run -v /mnt/c/Users/SequoiaAT/Desktop/Marva:/data $(IMAGE_NAME) cli-app-poetry --config $(CONFIG_PATH)



# Run tests
test:
	docker run $(IMAGE_NAME) pytest /app/tests

