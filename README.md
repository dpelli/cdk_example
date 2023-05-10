:warning: Work in Progress :warning:
# Welcome to my AWS API Gateway CDK Example

## Description

This project was created with the intent of experimenting with AWS CDK and API Gateway with Lambda integrations. I especially wanted to play around with static html hosting via lambda functions to facilitate a simple form for users.

I also wanted to experiment was CDK project structures, hoping to find the simplest, cleanest strategy for building lambda layers and maintaining the same import hierarchy both within the local CDK environment and the AWS console, without cluttering the project.

## Installation

### Pre-requisites
* Docker
* AWS CDK
* poetry
* Make

## Poetry
This project utilizes Poetry for to declare, manage, and install dependencies. 

Official documentation: https://python-poetry.org/docs/

### To install Poetry:
Linux, macOS, Windows (WSL)
```
curl -sSL https://install.python-poetry.org | python3 -
```

Windows (Powershell)
```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Useful commands
 * `poetry install` reads the pyproject.toml, resolves the dependencies, and installs them
 * `poetry update` gets the latest versions of the dependencies and updates poetry.lock
 * `poetry lock` locks (without installing) the dependencies specified in pyproject.toml
 * `poetry add {package-name}` adds required packages to pyproject.toml and installs them
 * `poetry remove {package-name}` removes a package from the current list of installed packages

## Makefile

The Makefile should be configured locally to match the appropriate aws-runas profile

```
deploy:
	make build
	aws-runas {profile} cdk deploy
```
#### Windows install:


```
choco install make
```

Useful commands

 * `make deploy` runs 'make build' then deploys the stack to the AWS account/region indicated by the profile designated within the Makefile
 * `make build` exports 'service' directory and lambda dependencies to ./build in order to create layers and lambda containers


## AWS CDK (Cloud Development Kit)
Official documentation: https://docs.aws.amazon.com/cdk/v2/guide/home.html
 
Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


## Credits

* [AWS Lambda Handler Cookbook (Python)](https://github.com/ran-isenberg/aws-lambda-handler-cookbook)
