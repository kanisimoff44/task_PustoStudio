FROM python:3.11

RUN mkdir /test_task

WORKDIR /test_task

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /test_task/docker/*.sh