FROM python:3.5.9-slim-stretch
RUN apt-get update && apt-get install \
    vim python3-matplotlib curl gcc \
    procps -yqq
RUN pip install telepot psutil matplotlib
COPY setup/etc/servstatsbot.conf /etc/init/
COPY setup/bin/initialize.sh              /usr/local/bin/initialize
RUN chmod +x /usr/local/bin/initialize
WORKDIR /home/worker/servman/
CMD ["initialize"]