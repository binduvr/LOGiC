FROM python:3.6.9-slim-buster

WORKDIR /usr/app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install Unidecode

WORKDIR /usr/build

RUN apt update
RUN apt install -y wget

RUN wget https://dl.bintray.com/coin-or/download/Cbc-2.10.3-linux-x86_64-gcc4.8.tgz

RUN tar xvf Cbc-2.10.3-linux-x86_64-gcc4.8.tgz

RUN mv bin/cbc /bin
RUN mv bin/clp /bin

RUN mv lib/* /lib

RUN apt install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
RUN apt install -y texlive-science

EXPOSE 5000

WORKDIR /usr/app

COPY . .

CMD [ "python", "run.py" ]