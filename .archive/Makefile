# -*- mode:makefile; coding:utf-8 -*-

# Copyright (c) 2020 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

.ONESHELL:
SHELL := /bin/bash

SOURCE_INIT = /tmp/venv.oxp
SOURCE = $(SOURCE_INIT)/bin/activate

all: run

run: code-run-async

stop: docker-stop

docker-stop:
	-docker stop mycontainer
	
docker-clean: docker-stop
	-docker rm mycontainer

docker-build:  docker-clean
	docker build -t oxp-image .

docker-run: docker-build
	docker run -d --name mycontainer -p 8080:80 oxp-image
	
.SILENT: clean-venv
clean-venv:
	@printf "$(BLUE)=> remove venv\n"
	rm -fr $(SOURCE_INIT)

.SILENT: venv
venv:
	@printf "$(BLUE)=> create venv\n"
	if [ ! -d $(SOURCE_INIT) ]; then \
		python -m venv $(SOURCE_INIT); \
		source $(SOURCE); \
		pip install -r app/requirements.txt; \
	fi

pre-commit:
	source $(SOURCE); \
	pre-commit install

pre-commit-update:
	source $(SOURCE); \
	pre-commit autoupdate

install: venv
	source $(SOURCE); \
	python -m pip install  --upgrade pip setuptools; \
	python -m pip install . --upgrade --upgrade-strategy eager

code-format: pre-commit-update
	source $(SOURCE); \
	pre-commit run yapf --all-files

code-lint:
	source $(SOURCE); \
	pre-commit run flake8 --all-files

code-run: install
	source $(SOURCE); \
	cd app; \
	uvicorn main:app --reload --host 0.0.0.0

code-run-async: install
	source $(SOURCE); \
	cd app; \
	uvicorn main:app --reload --host 0.0.0.0 &
	
clean: clean-venv
	rm -f app/oscal.sqlite
	rm -fr oscal.sqlite
	rm -fr oxp_demo.egg-info
	rm -fr build
	
