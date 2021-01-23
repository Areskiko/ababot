FROM python:alpine
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./src/*.py ./
COPY requirements.txt ./
CMD ["python3", "discordBot.py"]