FROM archlinux
RUN pacman -Syu --noconfirm python-pip supervisor python-twisted
RUN python -m pip install py3tftp
EXPOSE 80
EXPOSE 69/udp
COPY scripts/ /scripts
COPY etc/ /etc
COPY netboot/ /netboot
VOLUME /data
CMD ["/usr/bin/supervisord"]
