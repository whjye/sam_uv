.PHONY: test build
test:
	uv run pytest tests/unit -v

build-dependency-layer:
	uv pip install layers/common layers/models --target packages_layers

build:
	uv export --frozen --no-dev --no-editable --all-groups -o requirements.txt
	uv pip install \
		--no-installer-metadata \
		--no-compile-bytecode \
		--python-platform x86_64-manylinux2014 \
		--python 3.12 \
		--target packages \
		-r requirements.txt
