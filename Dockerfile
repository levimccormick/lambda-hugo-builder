FROM ubuntu:16.10
RUN apt-get update && apt-get install -y python python-pip python-apt zip wget
RUN pip install --upgrade pip
RUN pip install virtualenv awscli

ADD ./build_entry.sh /build_entry.sh
RUN ["chmod", "+x", "/build_entry.sh"]
WORKDIR /tmp
