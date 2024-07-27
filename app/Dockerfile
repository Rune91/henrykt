FROM python:3.12 AS builder

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

#ENTRYPOINT ["python3"]
#CMD ["main.py"]
CMD ["python3", "-u", "main.py"]




FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /