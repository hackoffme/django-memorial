FROM python:3.10-alpine
WORKDIR /home/user/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000", "--noreload"]