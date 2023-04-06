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
	echo Backuping
	mkdir -p backup && \
	aws s3 cp --recursive s3://${AWS_S3_BUCKET} backup


.PHONY: restore
restore:
	echo Restoring
	aws s3 cp --recursive backup s3://${AWS_S3_BUCKET}


.PHONY: remove_data
remove_data:
	aws s3 rb s3://${AWS_S3_BUCKET} --force


.PHONY: full_deploy
full_deploy: deploy

.PHONY: full_remove
full_remove: backup_data remove_data remove

