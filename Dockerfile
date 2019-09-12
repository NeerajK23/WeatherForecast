FROM ubuntu:16.04

EXPOSE 5002

RUN apt-get update -y

RUN apt-get install -y \
    python3 \
    python-pip \
    python3-dev \
    build-essential

RUN apt-get install wget -y
COPY . /app
WORKDIR /app
RUN wget https://launchpad.net/python-weather-api/trunk/0.3.8/+download/pywapi-0.3.8.tar.gz
RUN tar -xvzf pywapi-0.3.8.tar.gz
RUN cd pywapi-0.3.8 \
    && python setup.py install
RUN cd ..
RUN pip install -r requirements.txt
RUN pip install bs4
RUN pip install requests
ENTRYPOINT ["python"]
CMD ["application.py"]
