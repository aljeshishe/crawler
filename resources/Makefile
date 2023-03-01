SHELL := /bin/bash

# convert json -> yaml -> .env
# If print to yaml directly there could be line split and incorrect values in .env
$(shell  sls print --path parent --format json | yq -p json | sed 's/: /=/g' > .env)
include .env


.PHONY: deploy
deploy:
	sls deploy

.PHONY: remove
remove:
	sls remove

FILES = hh.csv linkedin.csv

.PHONY: backup_data
backup_data:
	BACKUP_DIR=$(shell date +%Y-%m-%d_%H-%M-%S) && \
	echo Backup to: $$BACKUP_DIR && \
	mkdir -p ./$$BACKUP_DIR  && \
	for FILE in $(FILES); do \
		aws s3 cp s3://${AWS_S3_BUCKET}/$$FILE $$BACKUP_DIR/$$FILE; \
	done


.PHONY: restore_data
restore_data:
ifndef FROM
	@echo 'FROM is not defined (example FROM=2019-01-01_12-00-00))'
	exit 1
endif

	echo Restoring from: $$FROM && \
	for FILE in $(FILES); do \
		aws s3 cp $$FROM/$$FILE s3://${AWS_S3_BUCKET}/$$FILE ; \
	done


.PHONY: remove_data
remove_data:
	aws s3 rb s3://${AWS_S3_BUCKET} --force


.PHONY: full_deploy
full_deploy: deploy

.PHONY: full_remove
full_remove: backup_data remove_data remove

