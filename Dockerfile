FROM ubuntu:latest
LABEL authors="dimul"

ENTRYPOINT ["top", "-b"]