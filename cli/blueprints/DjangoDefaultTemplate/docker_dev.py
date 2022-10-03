DOCKER_DEV="""
FROM python:3.8.14-bullseye

WORKDIR /.

COPY . . 

RUN pip install -r  ./requirements/requirements.txt --upgrade pip 

EXPOSE 8000 

ENTRYPOINT [ "python" ]

CMD ["manage.py","runserver",--settings=$project.settings.dev,"0.0.0.0:8000"]
"""