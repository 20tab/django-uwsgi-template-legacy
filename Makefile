export SETTINGS={{ project_name }}.settings.testing

ci:
	( \
		virtualenv --python=python3.6 ${JENKINSBUILD_DIR}/{{ project_name }}; \
		source ${JENKINSBUILD_DIR}/{{ project_name }}/bin/activate; \
		pip install -U -r requirements/tests.txt; \
		flake8; \
		coverage run manage.py test --settings=${SETTINGS} --noinput; \
		coverage xml; \
	)

initalpha:
	( \
		@${MAKE} ci; \
		cd deploy && TARGET=alpha ansible-playbook -vv deploy.yaml --tags "init"; \
	)

alpha:
	( \
		@${MAKE} ci; \
		cd deploy && TARGET=alpha ANSIBLE_PYTHON_INTERPRETER="~/venvs/{{ project_name }}_alpha/bin/python" ansible-playbook -vv deploy.yaml; \
	)

test:
	( \
	    pip install -U -r requirements/tests.txt; \
		coverage run manage.py test --settings=${SETTINGS} --noinput; \
		coverage xml; \
	)