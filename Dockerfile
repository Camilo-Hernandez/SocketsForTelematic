# Launches Alpine OS, installs python3 in it and runs the hello.py after the container startup

# Based on the latest version of the alpine image
FROM alpine:latest 

# Responsible
MAINTAINER Camilo Hernandez Ruiz

# Updates the package index and installs python3 in the alpine container
RUN apk --update add python3
RUN apk add busybox-extras
# Copies the hello-docker.py file to the image
COPY MyChatRoom.py /
COPY SocketClientTCP.py /
# Executes python3 with /opt/hello-docker.py as the only parameter
#CMD ["MyChatRoom.py"]
#ENTRYPOINT ["python3"]