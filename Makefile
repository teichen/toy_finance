.PHONY: test

help:
	@echo "test - execute testing"

test:
	pytest request_test.py
	pytest bin/allocation_test.py
