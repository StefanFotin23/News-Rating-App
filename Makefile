APP_NAME=news-rating-app
DOCKERFILE_DIR=dockerfile
DOCKERFILE_MODEL=Dockerfile-app
DOCKERFILE_MODEL_BUILD=Dockerfile-model-build

.PHONY: build run clean all train

all:
	make build
	make train
	make run

build:
	docker build -t $(APP_NAME)-model -f $(DOCKERFILE_DIR)/$(DOCKERFILE_MODEL_BUILD) .
	docker build -t $(APP_NAME)-app -f $(DOCKERFILE_DIR)/$(DOCKERFILE_MODEL) .

train:
	docker run --rm -v $(shell pwd)/models:/app/models $(APP_NAME)-model

run:
	docker run --rm -v $(shell pwd)/models:/app/models $(APP_NAME)-app

clean:
	docker rmi $(APP_NAME)-app $(APP_NAME)-model || true
