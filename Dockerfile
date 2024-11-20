FROM python:3.12-bullseye
<<<<<<< HEAD
RUN apt-get update && apt-get install -y anki
WORKDIR /Devops
COPY . /Devops/
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
=======
WORKDIR /myapp
COPY . /myapp/
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
>>>>>>> 29a015c (first commit)
