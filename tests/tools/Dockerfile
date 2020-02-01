FROM ubuntu:xenial

RUN apt-get update \
 && apt-get install -y -q --no-install-recommends \
        locales \
        ant \
	ant-optional \
        unzip \
        wget \
        make \
        default-jdk \
        subversion \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

WORKDIR /root/optimade
COPY . .

CMD ["/bin/bash", "-c", "make distclean; make audit"]
