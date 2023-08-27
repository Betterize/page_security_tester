FROM python:3.11.5-slim-bullseye

RUN apt-get update
RUN apt-get install nmap -y

RUN apt-get install -y unzip

COPY wapiti-3.1.7.zip wapiti-3.1.7.zip

RUN unzip wapiti-3.1.7.zip
RUN apt-get install -y --fix-missing python3-venv libxml2 libxml2-dev libz-dev libxslt1-dev python3-dev gcc
RUN cd 'wapiti-3.1.7' && python3 setup.py install

WORKDIR /tests_runner
COPY . /tests_runner
RUN pip3 install --no-cache-dir -r /tests_runner/requirements.txt

# required by wapiti ssl module
RUN pip3 install humanize sslyze
RUN pip3 install pyOpenSSL==22.1 typing-extensions==4.4.0

CMD ["python3", "tests_runner/main.py"]