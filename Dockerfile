FROM python:3.10

ENV APP_HOME=/app

RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . $APP_HOME

RUN pip install -r deps/requirements.txt

EXPOSE 8001

CMD ['uvicorn', 'financesvc.main:app', '--port', '8001']
