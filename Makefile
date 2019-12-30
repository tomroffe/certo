### LOCAL PUSH INTERGRATION ###
NO_CACHE = false
GIT_VERSION = $(shell git rev-parse --short HEAD)
DOCKER_REPO = toptop
TAG = $(shell git describe --exact-match --tags $(shell git log -n1 --pretty='%h'))

build:
	docker build --build-arg version_tag=$(TAG) --tag $(DOCKER_REPO)/$(NAME):$(TAG) .
.PHONY: build

push:
	docker push $(DOCKER_REPO):$(NAME):$(TAG)
.PHONY: push

run:
	docker run --rm -it -p 8000:8000 -v $(pwd)/data:/data $(DOCKER_REPO)/$(NAME):$(TAG)
.PHONY: run

ver:
	@echo '$(NAME):$(TAG)'
.PHONY: ver

