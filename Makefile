.PHONY: validate test package

validate: test
	python3 -m tooling.contracts --source-root .

test:
	python3 -m unittest discover -s tests

package:
	python3 -m tooling.release --output-dir dist
