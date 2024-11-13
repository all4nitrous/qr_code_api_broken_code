FROM python:3.12-bullseye
RUN apt-get update && apt-get install -y anki
WORKDIR /Devops
COPY . /Devops/
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
