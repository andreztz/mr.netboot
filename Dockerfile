FROM archlinux
RUN pacman -Syu --noconfirm python-pip supervisor python-twisted
RUN python -m pip install py3tftp
EXPOSE 80
EXPOSE 69/udp
COPY bin/ /bin
COPY etc/ /etc  
VOLUME /data 
CMD ["/usr/bin/supervisord"]
