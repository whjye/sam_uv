.PHONY: build-%

build-%:
	uv lock
	uv export --frozen --no-dev --no-editable --all-groups -o $(ARTIFACTS_DIR)/requirements.txt
	uv pip install \
		--no-installer-metadata \
		--no-compile-bytecode \
		--python-platform x86_64-manylinux2014 \
		--python 3.12 \
		--target $(ARTIFACTS_DIR) \
		-r $(ARTIFACTS_DIR)/requirements.txt
	cp *.py "$(ARTIFACTS_DIR)"