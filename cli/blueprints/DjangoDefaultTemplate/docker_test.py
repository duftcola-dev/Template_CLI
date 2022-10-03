DOCKER_TEST="""
FROM python:3.8.14-bullseye

WORKDIR /.

COPY . . 

RUN pip install -r  ./requirements/requirements.txt --upgrade pip 

EXPOSE 8000 

ENTRYPOINT [ "python" ]

CMD ["manage.py","runserver",--settings=$project.settings.test,"0.0.0.0:8000"]
"""