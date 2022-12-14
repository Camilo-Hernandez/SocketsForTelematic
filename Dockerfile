# Launches Alpine OS, installs python3 in it and runs the hello.py after the container startup

# Based on the latest version of the alpine image
FROM alpine:latest 

# Responsible
LABEL manteiner="Camilo Hernandez Ruiz"

# Updates the package index, installs python3 in the alpine container and busybox-extras for telenet
RUN apk --update add python3 \
 && apk add busybox-extras
# Copies the hello-docker.py file to the image
COPY . /

# Executes python3 with /opt/hello-docker.py as the only parameter
#CMD ["python3","MyChatRoom.py"]
