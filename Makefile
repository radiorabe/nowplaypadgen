init:
	pip install -r requirements.txt

test:
	python -m unittest discover -v

api-doc:
	sphinx-apidoc -M -f -o docs/api nowplaypadgen
