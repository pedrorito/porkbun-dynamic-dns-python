FROM python:latest

WORKDIR /usr/app/src

COPY porkbun-ddns.py ./
COPY config.json ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python","-u","./porkbun-ddns.py"]