# If the first argument is "run"...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: run install

all: default

default: install run


install:
	
	uv install 
	
test:
	uv run pytest tests

lint:
	uv run ruff format src tests
	uv run ruff check src
	uv run ruff check tests
	uv run mypy src tests

