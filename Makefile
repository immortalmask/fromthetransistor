NATIVE_C_LABS = $(sort $(patsubst %/tests/test.c,%,$(wildcard labs/*/tests/test.c)))

.PHONY: help doctor validate test solutions references challenges notebooks native-tests-content c-tests c-tests-clean c-sanitize verify

help:
	@python3 ftt --help

doctor:
	@python3 ftt doctor

validate:
	@python3 ftt validate

test:
	@python3 -m unittest discover -s tests -t . -v

solutions:
	@python3 ftt check --all-solutions

references:
	@python3 tools/sync_references.py --check

challenges:
	@python3 tools/sync_challenges.py --check

notebooks:
	@python3 tools/check_notebooks.py

native-tests-content:
	@python3 tools/sync_native_c_tests.py --check

c-tests: native-tests-content
	@test "$(words $(NATIVE_C_LABS))" -eq 12 || { \
		echo "expected native C tests in 12 labs, found $(words $(NATIVE_C_LABS))"; \
		exit 1; \
	}
	@set -e; for lab in $(NATIVE_C_LABS); do \
		echo "==> $$lab"; \
		$(MAKE) --no-print-directory -C "$$lab" test; \
	done

c-tests-clean:
	@set -e; for lab in $(NATIVE_C_LABS); do \
		$(MAKE) --no-print-directory -C "$$lab" clean; \
	done

c-sanitize:
	@CC="$(CURDIR)/tools/cc-ubsan" python3 ftt check --all-solutions

verify: references challenges validate test solutions notebooks c-tests c-sanitize
