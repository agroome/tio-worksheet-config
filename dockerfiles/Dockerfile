FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3-pip 
	
RUN pip3 install pytenable pydantic pandas python-dotenv openpyxl click

WORKDIR /usr/src/app

ENV PATH "$PATH:/usr/bin/env/:/usr/src/app"

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

COPY .env tio-config.xlsx /usr/src/app

COPY tio-config/ /usr/src/app/

RUN ln -s ./cli.py tio-config

ENTRYPOINT ["python3", "tio-config"]
