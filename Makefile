export SETTINGS={{project_name}}.settings.testing
export SECRETKEY=$(shell python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
export USERNAME=$(shell whoami)

# use this command in continuous integration environment (es: jenkins)
ci:
	( \
		/bin/cp {{project_name}}/settings/secret.py.template {{project_name}}/settings/secret.py; \
		sed -i'.bak' -e 's/password/${PASSWORD}/g;s/secretkey/${SECRETKEY}/g;s/username/postgres/g' {{project_name}}/settings/secret.py; \
		virtualenv --python=python3.6 ${JENKINSBUILD_DIR}/{{project_name}}; \
		source ${JENKINSBUILD_DIR}/{{project_name}}/bin/activate; \
		pip install -U pip; \
		pip install -U -r requirements/tests.txt; \
		npm install; \
		npm run build; \
		flake8; \
		COVERAGE_FILE=.coverage.test coverage run manage.py test --settings=${SETTINGS} --noinput --parallel; \
		COVERAGE_FILE=.coverage.behave coverage run manage.py behave --settings=${SETTINGS}; \
		coverage combine; \
		coverage xml; \
	)

initalpha:
	( \
		cd deploy && TARGET=alpha ansible-playbook -vv deploy.yaml; \
	)

alpha:
	( \
		cd deploy && TARGET=alpha ansible-playbook -vv deploy.yaml --skip-tags "init"; \
	)

test:
	( \
		COVERAGE_FILE=.coverage.test coverage run manage.py test --settings=${SETTINGS} --noinput --keepdb; \
		COVERAGE_FILE=.coverage.behave coverage run manage.py behave --settings=${SETTINGS} --keepdb; \
		coverage combine; \
		coverage html; \
	)

dev:
	( \
		pip install -U pip==18.1 pip-tools; \
		pip-sync requirements/dev.txt; \
	)

# to pass optional parameters use as: make pip p='-P requests'
pip:
	( \
		pip install -U pip==18.1 pip-tools; \
		pip-compile $(p) --output-file requirements/common.txt requirements/common.ini; \
		pip-compile $(p) --output-file requirements/dev.txt requirements/dev.ini; \
		pip-compile $(p) --output-file requirements/prod.txt requirements/prod.ini; \
		pip-compile $(p) --output-file requirements/tests.txt requirements/tests.ini; \
	)\

npm:
	( \
		npm install; \
		npm run build; \
	)

