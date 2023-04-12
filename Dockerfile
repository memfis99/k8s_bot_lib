FROM python:3.9.16

WORKDIR /mb_bot

COPY  requirements.txt requirements.txt
RUN   pip3 install -r requirements.txt

RUN mkdir -p /mb_bot

COPY ./*.py /mb_bot/
COPY ./*.txt /mb_bot/
COPY ./kubectl /usr/local/bin/

CMD ["python3", "./bot_control_v12_add_checknode.py"]