FROM envoyproxy/envoy:latest

RUN apt-get update
RUN apt-get -q install -y python-dev python-pip
RUN pip install flask grpcio protobuf requests
RUN mkdir /code

ADD ./service.py /code
ADD ./start.sh /usr/local/bin/start_service.sh

RUN chmod u+x /usr/local/bin/start_service.sh
ENTRYPOINT /usr/local/bin/start_service.sh
