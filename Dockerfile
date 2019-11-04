FROM python:3

RUN pip3 install redis
RUN pip3 install pymongo
COPY ./server.py /

EXPOSE 9091
ENTRYPOINT ["python", "server.py"]
