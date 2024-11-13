FROM python:3.12-bullseye

WORKDIR /app

COPY Devops/requirements.txt .

RUN pip install -r requirements.txt

COPY Devops/ .

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]