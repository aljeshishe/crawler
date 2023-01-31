SHELL := /bin/bash

.PHONY: deploy
deploy:
	sls deploy

.PHONY: remove
remove:
	sls remove

.PHONY: backup_data
backup_data:
	BACKUP_DIR=$(shell date +%Y-%m-%d_%H-%M-%S) && \
	echo $$BACKUP_DIR && \
	mkdir -p ./$$BACKUP_DIR  && \
	aws s3 cp s3://dashboards-bucket-dev/hh.csv $$BACKUP_DIR/hh.csv  && \
	aws s3 cp s3://dashboards-bucket-dev/linkedin.csv $$BACKUP_DIR/linkedin.csv


.PHONY: remove_data
remove_data:
	aws s3 rb s3://dashboards-bucket-dev --force


.PHONY: full_deploy
full_deploy: deploy

.PHONY: full_remove
full_remove: backup_data remove_data remove

