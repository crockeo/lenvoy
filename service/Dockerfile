FROM envoyproxy/envoy-alpine:latest

RUN apk update && apk add python3 bash
RUN pip3 install Flask==1.0.2
RUN mkdir /code

ADD ./service.py /code
ADD ./start.sh /usr/local/bin/start_service.sh

RUN chmod u+x /usr/local/bin/start_service.sh
ENTRYPOINT /usr/local/bin/start_service.sh
