FROM python:3.12-bullseye
WORKDIR /Devops
COPY . /Devops/
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
