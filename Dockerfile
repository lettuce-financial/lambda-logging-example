### Use an appropriate version of Python
FROM python:3.12-slim-bullseye@sha256:14cfaa6a5550e132b5a50652113c73425d0657f67e7892d9da716d599a76d1b7 AS python

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update -y && \
    apt-get -qq install -y awscli docker.io >/dev/null

RUN --mount=type=cache,target=/root/.cache \
    pip install --quiet --upgrade awslambdaric

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie


### Install requirements
FROM python AS requirements
COPY requirements.txt /opt/project/
WORKDIR /opt/project
RUN --mount=type=cache,target=/root/.cache \
    pip install --quiet --disable-pip-version-check --requirement requirements.txt


### Install source
FROM requirements AS source
COPY pyproject.toml /opt/project/
COPY src /opt/project/src


### Build wheel
FROM source AS build

RUN --mount=type=cache,target=/root/.cache \
    pip install --quiet --disable-pip-version-check .[dist]
COPY README.md .version /opt/project/
COPY bin/build /opt/project/bin/

RUN /opt/project/bin/build


### Install package
FROM requirements AS install

COPY --from=build /opt/project/dist/*.whl /opt/project/dist/
RUN --mount=type=cache,target=/root/.cache \
    pip install --quiet --disable-pip-version-check dist/*.whl



### Define deploy command
FROM install AS deploy

COPY entrypoint.sh /opt/project/bin/entrypoint.sh
RUN chmod 755 /usr/bin/aws-lambda-rie /opt/project/bin/entrypoint.sh

ENTRYPOINT [ "/opt/project/bin/entrypoint.sh" ]
CMD ["example.app.handle"]
