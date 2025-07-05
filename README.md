# SAM with uv

Example repo setup for a SAM application with uv.

The repo contains two Lambda Functions with seperate dependency requirements, a common Lambda Layer for dependencies and another Lambda Layer for shared code (event models). 

Additionally, AWS Lambda Powertools as a Layer is used when deployed, and accessible as a dev dependency locally.

## Adding a Lambda Function or Layer

1. Create a new uv project:
  - Function - `uv init lambda/new_fn`
  - Layer - `uv init --lib layers/new_layer`
2. Add Function or Layer specific dependencies to the Function/Layer with `uv add --project lambda/new_fn <package>`
3. Add it as a workspace member `uv add lambda/new_fn` or `uv add layers/new_layer`
4. Add a Makefile to `uv` for builds under `lambda/new_fn/Makefile`or `layers/new_layer/Makefile`:

    ```Makefile
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
        cp *.py "$(ARTIFACTS_DIR)" # remove this layer for layers
    ```

5. Specify `template.yaml` to use the Makefile for `sam build`:

    ```yaml
    Resources:
      ...
      NewFn:
        Type: AWS::Serverless::Function
        Properties:
          CodeUri: lambda/new_fn
          ...
        Metadata:
          BuildMethod: makefile
      ...
      NewLayer:
        Type: AWS::Serverless::LayerVersion
        Properties:
          ContentUri: layers/new_layer
          ...
        Metadata:
          BuildMethod: makefile
    ```

6. `sam build` or `sam sync` with builds or syncs via uv ⚡

## SAM Build with Docker

1. Create a custom build container by extending the SAM Docker build image to install uv (see [Dockerfile](./Dockerfile)): `docker build -t public.ecr.aws/sam/build-python3.12_uv:latest-x86_64 .`
2. Build using this image `sam build --use-container --skip-pull-image --build-image public.ecr.aws/sam/build-python3.12_uv:latest-x86_64`

> [!WARNING]
> Building inside a container with a custom Makefile build will cause the cache to be invalid for Lambda Functions, increasing build time. Where possible, bundle common dependencies to a Lambda Layer.

## Further Reading

- [Building Lambda functions with custom runtimes in AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/building-custom-runtimes.html#building-custom-runtimes-examples) - example on Makefile builder rather than using bundled builder
- [Using uv with AWS Lambda](https://docs.astral.sh/uv/guides/integration/aws-lambda/) - details on how to build and deploy AWS Lambda with uv (without SAM)
- [Release 1.9.0 - Support for Cached and Parallel Builds](https://github.com/aws/aws-sam-cli/releases/tag/v1.9.0) - `sam build --cached` does not support custom builds with Makefile