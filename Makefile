.PHONY:  sort deps build deploy destroy

sort:
	isort ${PWD}

deps:
	poetry export --only=dev --without-hashes --format=requirements.txt > dev_requirements.txt
	poetry export --without=dev --without-hashes --format=requirements.txt > lambda_requirements.txt

build:
	make deps
	mkdir -p .build/lambdas ; cp -r service .build/lambdas
	mkdir -p .build/common_layer ; poetry export --without=dev --without-hashes --format=requirements.txt > .build/common_layer/requirements.txt

login:
	aws sso login --profile prod

deploy:
	make build
	cdk deploy --app="python3 ${PWD}/app.py" --require-approval=never --profile="prod"

destroy:
	cdk destroy --app="python3 ${PWD}/app.py" --force --profile="prod"