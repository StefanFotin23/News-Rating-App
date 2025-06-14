APP_NAME=news-rating-app
DOCKERFILE_DIR=docker
DOCKERFILE_MODEL=Dockerfile

.PHONY: status get-namespaces get-configmaps get-deployments get-pods get-svc build-image clean apply port-forward update-image restart delete

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
	docker tag news-rating-app stefanfotin23/news-rating-app
	docker push stefanfotin23/news-rating-app

all:
	kind create cluster
	make build-image
	make apply
	
port-forward:
	kubectl port-forward svc/news-rating-service 8080:80 &

update-image:
	make build-image
	kubectl set image deployment/news-rating-app news-rating-app=stefanfotin23/news-rating-app
	make restart

delete:
	kubectl delete pods -l app=news-rating

restart:
	kubectl rollout restart deployment news-rating-app

logs:
	kubectl get pods -l app=news-rating -o name | xargs -n1 kubectl logs

apply:
	kubectl apply -R -f k8s/

clean:
	docker rmi $(APP_NAME) || true
	kind delete cluster
