FROM python:3.11.0rc2-alpine3.16
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
EXPOSE 80
EXPOSE 69/udp
COPY scripts/ /scripts
COPY etc/ /etc
COPY netboot/ /netboot
VOLUME /data
WORKDIR / 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# CMD ["/usr/bin/supervisord"]
CMD ["/usr/local/bin/supervisord"]

