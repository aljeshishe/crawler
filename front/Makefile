SHELL := /bin/bash
# SHELL:=/usr/bin/env bash

# convert json -> yaml -> .env
# If print to yaml directly there could be line split and incorrect values in .env
$(shell  sls print --path parent --format json | yq -p json | sed 's/: /=/g' > .env)
include .env

export AWS_PAGER=""

export
.PHONY: install
install:
	# login and create private ECR repository if not exists
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${REMOTE_MACHINE}
	aws ecr describe-repositories --repository-names ${REPO_NAME} || aws ecr create-repository --repository-name ${REPO_NAME}

	# login and create public ECR repository if not exists
	# aws ecr-public create-repository --repository-name ${REPO_NAME} --region us-east-1 || true
	# aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

.PHONY: uninstall
uninstall:
	# aws ecr list-images --repository-name ${IMAGE_NAME} --query 'imageIds[*][imageDigest]' --output text | while read imageId; do aws ecr batch-delete-image --repository-name ${IMAGE_NAME} --image-ids imageDigest=$imageId; done
	# aws ecr delete-repository --repository-name ${REPO_NAME} --force

.PHONY: build
build:
	poetry export -f requirements.txt -o requirements.txt --only=main
	docker build --progress=plain -t ${LOCAL_IMAGE} .

.PHONY: push
push:
	docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
	docker push ${REMOTE_IMAGE}

.PHONY: cisetup
cisetup:
	poetry install --only dev

.PHONY: pdv
pdv: cisetup
	poetry run python pdv.py

.PHONY: deploy
deploy:
	sls deploy

.PHONY: remove
remove:
	sls remove

.PHONY: logs
logs:
	sls logs --function func

.PHONY: full_deploy
full_deploy: install build push deploy pdv

.PHONY: full_remove
full_remove: remove uninstall


