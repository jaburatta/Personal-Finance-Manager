FROM python:3.8

WORKDIR /usr/src/app 

EXPOSE 5000

COPY requirements.txt /usr/src/app

RUN pip install -r requirements.txt

RUN python -m spacy download en

RUN python -m spacy download en_core_web_sm

COPY  . /usr/src/app

CMD [ "python", "application.py"]