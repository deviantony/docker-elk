# Copyright The OpenTelemetry Authors
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

# All documents to be used in spell check.
ALL_DOCS := $(shell find . -type f -name '*.md' -not -path './.github/*' -not -path '*/node_modules/*' -not -path '*/_build/*' -not -path '*/deps/*' | sort)
PWD := $(shell pwd)

TOOLS_DIR := ./internal/tools
MISSPELL_BINARY=bin/misspell
MISSPELL = $(TOOLS_DIR)/$(MISSPELL_BINARY)

# see https://github.com/open-telemetry/build-tools/releases for semconvgen updates
# Keep links in semantic_conventions/README.md and .vscode/settings.json in sync!
SEMCONVGEN_VERSION=0.11.0

# TODO: add `yamllint` step to `all` after making sure it works on Mac.
.PHONY: all
all: install-tools markdownlint misspell

$(MISSPELL):
	cd $(TOOLS_DIR) && go build -o $(MISSPELL_BINARY) github.com/client9/misspell/cmd/misspell

.PHONY: misspell
misspell:	$(MISSPELL)
	$(MISSPELL) -error $(ALL_DOCS)

.PHONY: misspell-correction
misspell-correction:	$(MISSPELL)
	$(MISSPELL) -w $(ALL_DOCS)

.PHONY: markdownlint
markdownlint:
	@if ! npm ls markdownlint; then npm install; fi
	@for f in $(ALL_DOCS); do \
		echo $$f; \
		npx --no -p markdownlint-cli markdownlint -c .markdownlint.yaml $$f \
			|| exit 1; \
	done

.PHONY: install-yamllint
install-yamllint:
    # Using a venv is recommended
	pip install -U yamllint~=1.30.0

.PHONY: yamllint
yamllint:
	yamllint .

# Run all checks in order of speed / likely failure.
.PHONY: check
check: misspell markdownlint
	@echo "All checks complete"

# Attempt to fix issues / regenerate tables.
.PHONY: fix
fix: misspell-correction
	@echo "All autofixes complete"

.PHONY: install-tools
install-tools: $(MISSPELL)
	npm install
	@echo "All tools installed"

.PHONY: build-and-push-dockerhub
build-and-push-dockerhub:
	docker compose --env-file .dockerhub.env -f docker-compose.yml build
	docker compose --env-file .dockerhub.env -f docker-compose.yml push

.PHONY: build-and-push-ghcr
build-and-push-ghcr:
	docker compose --env-file .ghcr.env -f docker-compose.yml build
	docker compose --env-file .ghcr.env -f docker-compose.yml push

.PHONY: build-env-file
build-env-file:
	cp .env .dockerhub.env
	sed -i '/IMAGE_VERSION=.*/c\IMAGE_VERSION=${RELEASE_VERSION}' .dockerhub.env
	sed -i '/IMAGE_NAME=.*/c\IMAGE_NAME=${DOCKERHUB_REPO}' .dockerhub.env
	cp .env .ghcr.env
	sed -i '/IMAGE_VERSION=.*/c\IMAGE_VERSION=${RELEASE_VERSION}' .ghcr.env
	sed -i '/IMAGE_NAME=.*/c\IMAGE_NAME=${GHCR_REPO}' .ghcr.env

run-tests:
	docker compose run frontendTests
	docker compose run integrationTests

.PHONY: generate-protobuf
generate-protobuf:
	./ide-gen-proto.sh

.PHONY: generate-kubernetes-manifests
generate-kubernetes-manifests:
	helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
	helm repo update
	helm template opentelemetry-demo open-telemetry/opentelemetry-demo | sed '/helm.sh\/chart\:/d' | sed '/helm.sh\/hook/d' | sed '/managed-by\: Helm/d' > kubernetes/opentelemetry-demo.yaml
