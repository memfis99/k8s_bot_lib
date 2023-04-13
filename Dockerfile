FROM python:3.9.16

WORKDIR /mb_bot

COPY  requirements.md requirements.txt
RUN   pip3 install -r requirements.txt

RUN mkdir -p /mb_bot

COPY ./*.py /mb_bot/
COPY ./internal/*.py /mb_bot/




CMD ["python3", "./bot_control_lib_v1.py"]