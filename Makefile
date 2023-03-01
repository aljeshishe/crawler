SHELL:=/usr/bin/env bash
echo_target=@echo -n '[$@]: ' && echo $(1) && echo -n '[$@]: ' && $(1)

SUBDIRS = resources collector front

include .secretenv
export

ifneq ($(dir),)
SUBDIRS := $(dir)
endif

.PHONY: full_deploy
full_deploy:
	for dir in $(SUBDIRS); do \
    echo "[$$dir]: make $@"; \
    $(MAKE) --directory=$$dir $@; \
	done

.PHONY: full_remove
full_remove:
	for dir in $(SUBDIRS); do \
    echo "[$$dir]: make $@"; \
    $(MAKE) --directory=$$dir $@; \
	done


.PHONY: build
build:
	for dir in $(SUBDIRS); do \
    $(MAKE) --directory=$$dir $@; \
	done

.PHONY: push
push:
	for dir in $(SUBDIRS); do \
    $(MAKE) --directory=$$dir $@; \
	done

.PHONY: pdv
pdv:
	for dir in $(SUBDIRS); do \
    $(MAKE) --directory=$$dir $@; \
	done

.PHONY: ja
ja:
	$(call echo_target, echo "Hello World!")
	for i in {0..100}; do echo a-$$i; sleep 1 ; done
.PHONY: jb
jb:
	$(call echo_target, echo "Hello World!")
	for i in {0..100}; do echo b-$$i; sleep 1 ; done

.PHONY: j
j: ja jb

.PHONY: ci
ci: full_deploy full_remove

#.DEFAULT:
#	@cd docs && $(MAKE) $@


