ARG PYTHON_IMAGE=python:3.10-slim

from $PYTHON_IMAGE as build
ARG PAGE_ID
ARG INTEGRATION_TOKEN
#install
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false
WORKDIR /app
COPY pyproject.toml pdm.lock README.md .
COPY ./notion_graph ./notion_graph
RUN pdm install
#run
RUN pdm run start -p $PAGE_ID -t $INTEGRATION_TOKEN -o ./graph_out.html > ./log.txt 2>&1 


FROM nginx:alpine as expose
COPY --from=build /app/graph_out.html /usr/share/nginx/html/index.html
COPY --from=build /app/log.txt /usr/share/nginx/html/log.txt
EXPOSE 80