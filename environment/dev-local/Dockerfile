FROM gcr.io/bgds-development/bgds/base-environment:0.1

# DB connection information
ENV CARAVAGGIO_DOMAIN http://caravaggio:8000
ENV CARAVAGGIO_TOKEN cb31a1546c70841f43512df1435b24f4ccbcbc67

RUN mkdir /caravaggio-python-binding

ADD . /caravaggio-python-binding/

RUN cd /caravaggio-python-binding && python setup.py develop
RUN cd /caravaggio-python-binding && pip install -r requirements_docs.txt || echo "ignore error"
RUN cd /caravaggio-python-binding && pip install -r requirements_tests.txt || echo "ignore error"

RUN mkdir -p /data/bgds_caravaggio_binding/log

WORKDIR /caravaggio-python-binding

VOLUME /caravaggio-python-binding

RUN mkdir /initial_data

VOLUME /initial_data

CMD tail -f /dev/null