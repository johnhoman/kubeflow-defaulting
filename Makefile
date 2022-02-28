fmt:
	python -m black src
test: fmt
	python -m pytest src
