.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run:	## Start server
	python3 manage.py runserver

.PHONY: shell
shell:	## Start Shell
	python3 manage.py shell

.PHONY: migrate
migrate: ## Apply migration(s) to database
	python3 manage.py migrate

.PHONY: migrations
migrations:  ## Create new migration(s)
	python3 manage.py makemigrations

.PHONY: test
test:	## Run project tests
	python3 manage.py test

.PHONY: requirements
requirements:	## Run project tests
	pip freeze > requirements.txt
