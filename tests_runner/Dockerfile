FROM python:3.11.4-slim-bullseye

RUN apt-get update
RUN apt-get install nmap -y

RUN apt-get install -y unzip

COPY wapiti-3.1.7.zip wapiti-3.1.7.zip

RUN unzip wapiti-3.1.7.zip
RUN pip3 install sslyze
RUN apt-get install -y python3-venv libxml2 libxml2-dev libz-dev libxslt1-dev python3-dev gcc
RUN cd 'wapiti-3.1.7' && python3 setup.py install

WORKDIR /tests_runner
COPY . /tests_runner
RUN pip3 install --no-cache-dir -r /tests_runner/requirements.txt

CMD ["python3", "tests_runner/main.py"]