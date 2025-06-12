FROM debian:bookworm

WORKDIR /VMapp

COPY requirements.txt .

RUN apt update && apt install -y --no-install-recommends gnupg

RUN echo "deb http://archive.raspberrypi.org/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

RUN apt update && apt -y upgrade

RUN apt update && apt install -y --no-install-recommends \
         python3-pip \
         python3-picamera2 \
     && apt-get clean\
     && apt-get autoremove \
     && rm -rf /var/cache/apt/archives/* \
     && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y --no-install-recommends gnupg build-essential cmake ninja-build python3-dev
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

RUN pip3 install --break-system-packages --no-cache-dir rpi.gpio

COPY ./src ./src

CMD ["python3", "./src/Main.py"]