FROM debian:buster
MAINTAINER Peter Willemsen <peter@codebuffet.co>
RUN echo "Installing dependencies..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl sudo git build-essential cmake python3-pip python3 pkg-config libssl-dev zsh clang && \
    apt-get dist-upgrade -y && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install jupyterlab terra-sdk
WORKDIR /opt/terra_bot

# Add dev user
RUN useradd -ms /bin/zsh terra-dev && \
    usermod -aG sudo terra-dev && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER terra-dev

CMD ["jupyter", "lab", "--ip=0.0.0.0"]