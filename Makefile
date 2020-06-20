default: test

clean:
	rm -rf unfun_html/__pycache__ tests/__pycache__ dist/ unfun_html.egg-info/ build/

package:
	python setup.py sdist bdist_wheel

pypi-upload-test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-upload:
	python3 -m twine upload dist/*

test:
	python --version
	python -m pytest tests/
	autopep8 --max-line-length 99  --diff -r unfun_html/ tests/ | colordiff
	flake8 --builtins="_" --max-line-length 99 unfun_html/ tests/
	pylint unfun_html/ tests/*.py  --good-names 'f,i'
