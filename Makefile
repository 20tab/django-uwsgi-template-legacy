export SETTINGS={{ project_name }}.settings.testing

ci:
	( \
		virtualenv --python=python3.6 ${JENKINSBUILD_DIR}/{{ project_name }}; \
		source ${JENKINSBUILD_DIR}/{{ project_name }}/bin/activate; \
		pip install -U pip pip-tools; \
		pip-sync requirements/tests.txt; \
		flake8; \
		coverage run manage.py test --settings=${SETTINGS} --noinput; \
		coverage xml; \
		python manage.py behave --settings=${SETTINGS}; \
	)

initalpha:
	( \
		@${MAKE} ci; \
		cd deploy && TARGET=alpha ansible-playbook -vv deploy.yaml --tags "init"; \
	)

alpha:
	( \
		@${MAKE} ci; \
		cd deploy && TARGET=alpha ansible-playbook -vv deploy.yaml; \
	)

test:
	( \
		pip install -U pip pip-tools; \
		pip-sync requirements/tests.txt; \
		python manage.py test --settings=${SETTINGS} --noinput --keepdb --parallel; \
		python manage.py behave --settings=${SETTINGS} --keepdb; \
	)

dev:
	( \
		pip install -U pip pip-tools; \
		pip-sync requirements/dev.txt; \
	)

# to pass optional parameters use as: make pip p='-P requests'
pip:
	( \
		pip install -U pip pip-tools; \
		pip-compile $(p) --output-file requirements/common.txt requirements/common.ini; \
		pip-compile $(p) --output-file requirements/deploy.txt requirements/deploy.ini; \
		pip-compile $(p) --output-file requirements/dev.txt requirements/dev.ini; \
		pip-compile $(p) --output-file requirements/prod.txt requirements/prod.ini; \
		pip-compile $(p) --output-file requirements/tests.txt requirements/tests.ini; \
	)
