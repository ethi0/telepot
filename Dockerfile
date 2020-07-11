FROM python:3.5.9-slim-stretch
RUN apt-get update && apt-get install \
    vim python3-matplotlib curl gcc \
    procps nmap portaudio19-dev python3-pyaudio -yqq
RUN pip install telepot psutil requests PyMySql python3-wget curl2 noise-detector
COPY setup/etc/servstatsbot.conf /etc/init/
COPY setup/etc/vimrc             /root/.vimrc
COPY setup/bin/initialize.sh              /usr/local/bin/initialize
RUN chmod +x /usr/local/bin/initialize
WORKDIR /home/worker/servman/
SHELL [ "/bin/bash" ]
CMD ["initialize"]