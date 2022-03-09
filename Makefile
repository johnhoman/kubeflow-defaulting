IMG ?= jackhoman/kubeflow-defaulting:$(shell git describe --tags --always --dirty | sed 's/^v//g')

requirements:
	pip-compile requirements.in -o requirements.txt

build-image: requirements
	docker build -t ${IMG} -f Dockerfile .

run-image: build-image
	docker run --rm -it -p 8000:8000 ${IMG}

fmt:
	python -m black src
test: fmt
	python -m pytest src
