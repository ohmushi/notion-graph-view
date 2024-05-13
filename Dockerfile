ARG PYTHON_IMAGE=python:3.10-slim

from $PYTHON_IMAGE as build
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false
WORKDIR /app
COPY . .
RUN pdm install
CMD pdm run web
EXPOSE 3000
