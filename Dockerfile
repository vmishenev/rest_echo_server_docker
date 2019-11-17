FROM python:3

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./server.py /

EXPOSE 9091
ENTRYPOINT ["python", "server.py"]
