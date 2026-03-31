FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/home/standart

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
      python3-venv \
      python3-tk \
      ffmpeg \
      xvfb \
      xauth \
      cargo \
      rustc \
      pkg-config \
      libdbus-1-dev \
      make \
      tmux \
      git \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/desktop-markdown-sync
COPY . /opt/desktop-markdown-sync
RUN mkdir -p /home/standart/subprojects /artifacts

ENTRYPOINT ["bash"]
