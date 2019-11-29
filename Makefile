Makefile### LOCAL PUSH INTERGRATION ###
NO_CACHE = false
GIT_VERSION = $(shell git rev-parse --short HEAD)
APP_IMAGE = $(NAME):$(GIT_VERSION)

### AWS PUSH INTERGRATION ###
# CLUSTER = ecs-cluster-name
# ECR_REGION = eu-west-1
# ECR_ACCOUNT_NUMBER = 123456789123
# ECR_REPO = $(ECR_ACCOUNT_NUMBER).dkr.ecr.$(ECR_REGION).amazonaws.com
# APP_IMAGE = $(ECR_REPO)/$(NAME):$(VERSION)

build:
	docker build -t $(NAME):$(GIT_VERSION) .
	# docker tag $(NAME):$(GIT_VERSION) $(APP_IMAGE)
.PHONY: build

push:
	#$(shell aws ecr get-login --no-include-email --region eu-west-1)
	docker push $(APP_IMAGE)
	#aws ecs update-service --cluster $(CLUSTER) --service $(NAME) --force-new-deployment
.PHONY: push

ver:
	@echo '$(NAME):$(GIT_VERSION)'
.PHONY: ver

