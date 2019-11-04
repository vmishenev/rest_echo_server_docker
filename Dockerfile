FROM python:3

RUN pip3 install redis
RUN pip3 install pymongo
RUN pip3 install web.py
RUN pip3 install requests
COPY ./server.py /

EXPOSE 9091
ENTRYPOINT ["python", "server.py"]
