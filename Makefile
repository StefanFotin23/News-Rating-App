APP_NAME=news-rating-app
DOCKERFILE_DIR=docker
DOCKERFILE_MODEL=Dockerfile

.PHONY: status get-namespaces get-configmaps get-deployments get-pods get-svc build-image clean apply

status: get-namespaces get-configmaps get-deployments get-pods get-svc

get-namespaces:
	kubectl get namespaces
	@echo "\n"

get-configmaps:
	kubectl get configmaps --all-namespaces
	@echo "\n"

get-deployments:
	kubectl get deployments --all-namespaces
	@echo "\n"

get-pods:
	kubectl get pods --all-namespaces
	@echo "\n"

get-svc:
	kubectl get svc --all-namespaces
	@echo "\n"

build-image:
	docker build -t $(APP_NAME) -f $(DOCKERFILE_DIR)/$(DOCKERFILE_MODEL) .

all:
	kind create cluster
	make apply

apply:
	kubectl apply -R -f k8s/

clean:
	docker rmi $(APP_NAME) || true
