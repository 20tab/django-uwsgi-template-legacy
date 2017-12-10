export SETTINGS={{ project_name }}.settings.testing

ci:
	( \
		virtualenv --python=python3.6 ${JENKINSBUILD_DIR}/{{ project_name }}; \
		source ${JENKINSBUILD_DIR}/{{ project_name }}/bin/activate; \
		pip install -r requirements.txt; \
		pycodestyle; \
		coverage run --source='.' manage.py test tests --settings=${SETTINGS}; \
	)

deploy:
	@${MAKE} ci
	echo "sto eseguendo il deploy"
