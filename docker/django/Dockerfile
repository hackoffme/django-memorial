FROM python:3.10-alpine
WORKDIR /home/user/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN python -m pip install --upgrade pip

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
# COPY entrypoint.sh .
# RUN chmod +x entrypoint.sh
# RUN sh entrypoint.sh
# COPY . .
# RUN python manage.py migrate

# COPY . .
# CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000", "--noreload"]