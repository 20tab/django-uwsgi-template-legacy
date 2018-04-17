export SETTINGS={{ project_name }}.settings.testing

ci:
	( \
		virtualenv --python=python3.6 ${JENKINSBUILD_DIR}/{{ project_name }}; \
		source ${JENKINSBUILD_DIR}/{{ project_name }}/bin/activate; \
		pip install -U -r requirements/tests.txt; \
		flake8; \
		coverage run --source='.' manage.py test --settings=${SETTINGS} --noinput; \
		coverage xml; \
		python manage.py behave --settings=${SETTINGS}; \
	)

alpha:
	( \
		@${MAKE} ci; \
		cd deploy && TARGET=alpha ansible-playbook -vv deploy.yaml; \
	)
