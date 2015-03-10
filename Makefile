help:
	@echo 'dev        - install dev requirements'
	@echo 'prod       - install prod requirements'
	@echo 'venv       - create virtualenv venv-folder'
	@echo 'production - deploy production (used by chewie)'

dev:
	pip install -r requirements/dev.txt --upgrade

prod:
	pip install -r requirements/prod.txt --upgrade

isort:
	isort -rc noetikon

noetikon/settings/local.py:
	touch noetikon/settings/local.py

production:
	git fetch && git reset --hard origin/master
	venv/bin/pip install -Ur requirements/prod.txt --upgrade
	venv/bin/python manage.py migrate
	venv/bin/python manage.py collectstatic --noinput
	sudo supervisorctl restart noetikon

.PHONY: help dev prod production isort
