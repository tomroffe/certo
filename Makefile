### LOCAL PUSH INTERGRATION ###
NO_CACHE = false
GIT_VERSION = $(shell git rev-parse --short HEAD)
DOCKER_REPO = toptop
APP_IMAGE = $(NAME):$(GIT_VERSION)

build:
	docker build -t $(DOCKER_REPO):$(NAME):0.0.1 .
.PHONY: build

push:
	docker push $(APP_IMAGE)
.PHONY: push

run:
	docker run --rm -it -p 8000:8000 -v $(pwd)/data:/data toptop/procudo:0.0.1
.PHONY: run

ver:
	@echo '$(NAME):$(GIT_VERSION)'
.PHONY: ver

