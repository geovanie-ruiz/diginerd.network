FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code
COPY requirements.txt /code/
COPY entrypoint.sh /entrypoint.sh
RUN pip install --upgrade pip
RUN pip install -r requirements.txt