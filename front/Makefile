SHELL:=/usr/bin/env bash

include .env
export

.PHONY: setdown
setdown:
 aws ecr list-images --repository-name ${IMAGE_NAME} --query 'imageIds[*][imageDigest]' --output text | \
 	while read imageId; do aws ecr batch-delete-image --repository-name ${IMAGE_NAME} --image-ids imageDigest=$imageId; done

.PHONY: build
build:
	poetry export -f requirements.txt -o requirements.txt --only=main
	sls wsgi install
	docker build --progress=plain -t ${LOCAL_IMAGE} .

.PHONY: push
push:
	# get password from aws and login to ECR
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT}.dkr.ecr.eu-central-1.amazonaws.com
	# create ECR repository if not exists
	aws ecr describe-repositories --repository-names ${IMAGE_NAME} || aws ecr create-repository --repository-name ${IMAGE_NAME}
	docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
	docker push ${REMOTE_IMAGE}


.PHONY: pdv
pdv:
	python runner.py

.PHONY: deploy
deploy:
	sls deploy

.PHONY: full_deploy
full_deploy: build push deploy pdv

.PHONY: lint
lint:
	poetry run mypy crawler tests/**/*.py
	poetry run flake8 .
	poetry run doc8 -q docs

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package unit

.DEFAULT:
	@cd docs && $(MAKE) $@



