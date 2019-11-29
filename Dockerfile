FROM python:3.7.4-stretch

LABEL maintainer="tom@sm4rt.io"
LABEL "com.example.vendor"="sm4rt"
LABEL version="0.1"
LABEL description="Generates OpenVPN Config File (ovpn), \
cert and keys must exisit in /etc/openvpn/pki/"

RUN mkdir -p /templates /data
ADD templates /templates/
ADD app.py /
ADD requirements.txt /

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
