SHELL := /bin/bash

# convert json -> yaml -> .env
# If print to yaml directly there could be line split and incorrect values in .env
$(shell  sls print --path parent --format json | yq -p json | sed 's/: /=/g' > .env)
include .env

export AWS_PAGER=""

export

.PHONY: logs
logs:
	sls logs --function function

.PHONY: install
install:
	# login and create private ECR repository if not exists
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${REMOTE_MACHINE}
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
	#
	aws ecr describe-repositories --repository-names ${IMAGE_NAME} || aws ecr create-repository --repository-name ${IMAGE_NAME}

	# login and create public ECR repository if not exists
	# aws ecr-public create-repository --repository-name ${IMAGE_NAME} --region us-east-1 || true

.PHONY: uninstall
uninstall:
	aws ecr list-images --repository-name ${IMAGE_NAME} --query 'imageIds[*][imageDigest]' --output text | while read imageId; do aws ecr batch-delete-image --repository-name ${IMAGE_NAME} --image-ids imageDigest=$imageId; done
	aws ecr delete-repository --repository-name ${IMAGE_NAME} --force

.PHONY: build
build:
	poetry export -f requirements.txt -o requirements.txt --only=main
	docker build --progress=plain -t ${LOCAL_IMAGE} .

.PHONY: push
push:
	docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
	docker push ${REMOTE_IMAGE}

.PHONY: pdv
pdv:
	python pdv.py

.PHONY: deploy
deploy:
	sls deploy

.PHONY: remove
remove:
	sls remove

.PHONY: full_deploy
full_deploy: install build push deploy pdv

.PHONY: full_remove
full_remove: remove uninstall

.PHONY: test
test:
	pytest

