FROM python:3
ADD . /chroot
WORKDIR /chroot
RUN pip install -r deps/prod.txt
