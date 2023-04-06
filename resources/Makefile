SHELL := /bin/bash

$(V).SILENT:

# convert json -> yaml -> .env
# If print to yaml directly there could be line split and incorrect values in .env
$(shell  sls print --path parent --format json | yq -p json | sed 's/: /=/g' > .env)
$(shell  cat ../.secretenv >> .env)
include .env
export

.PHONY: deploy
deploy:
	sls deploy

.PHONY: remove
remove:
	sls remove

FILES = hh.csv linkedin.csv

.PHONY: backup
backup:
	BACKUP_DIR=$$(realpath backup) && \
	echo Backup to: $$BACKUP_DIR && \
	mkdir -p ./$$BACKUP_DIR  && \
	for FILE in $(FILES); do \
		aws s3 cp s3://${AWS_S3_BUCKET}/$$FILE $$BACKUP_DIR/$$FILE; \
	done


.PHONY: restore
restore:
	BACKUP_DIR=$$(realpath backup) && \
	echo Restoring from: $$BACKUP_DIR && \
	for FILE in $(FILES); do \
		aws s3 cp $$BACKUP_DIR/$$FILE s3://${AWS_S3_BUCKET}/$$FILE ; \
	done


.PHONY: remove_data
remove_data:
	aws s3 rb s3://${AWS_S3_BUCKET} --force


.PHONY: full_deploy
full_deploy: deploy

.PHONY: full_remove
full_remove: backup_data remove_data remove

