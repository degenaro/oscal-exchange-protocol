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

all: run

run: code-run

stop: docker-stop

docker-stop:
	-docker stop mycontainer
	
docker-clean: docker-stop
	-docker rm mycontainer

docker-build:  docker-clean
	docker build -t oxp-image .

docker-run: docker-build
	docker run -d --name mycontainer -p 8080:80 oxp-image
	
venv:
	python -m venv venv.oxp
	. ./venv.oxp/bin/activate

pre-commit: 
	pre-commit install

pre-commit-update:
	pre-commit autoupdate

install: venv
	python -m pip install  --upgrade pip setuptools
	python -m pip install . --upgrade --upgrade-strategy eager

code-format: pre-commit-update
	pre-commit run yapf --all-files

code-lint:
	pre-commit run flake8 --all-files

code-run: install
	cd app
	uvicorn main:app --reload --host 0.0.0.0

code-run-daemon: install
	cd app
	uvicorn main:app --reload --host 0.0.0.0 &
	
clean:
	rm -f app/oscal.sqlite
	rm -fr oscal.sqlite
	rm -fr venv.oxp
	rm -fr oxp_demo.egg-info
	rm -fr build
