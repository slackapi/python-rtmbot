FROM python:2.7-slim
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
CMD python rtmbot.py
