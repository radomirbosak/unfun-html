TEST_WORDS = Petersilie Kragen

default: test check

clean:
	rm -rf unfun_html/__pycache__ tests/__pycache__ dist/ unfun_html.egg-info/ build/

package:
	python setup.py sdist bdist_wheel

pypi-upload-test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-upload:
	python3 -m twine upload dist/*

check:
	autopep8 --max-line-length 99  --diff -r unfun_html/ tests/ | colordiff
	flake8 --builtins="_" --max-line-length 99 unfun_html/ tests/
	pylint unfun_html/ tests/ --good-names 'f,i'

test: test-unit test-word

test-word:
	python -m pytest tests/word -v

test-unit:
	python -m pytest tests/unit -v

download-data:
	for word in ${TEST_WORDS} ; do \
		./tools/download_word.sh $$word ; \
	done
