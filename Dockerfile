FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN git clone https://github.com/JishuDeveloper/Ultra-Forward-Bot /Ultra-Forward-Bot
WORKDIR /Ultra-Forward-Bot
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
