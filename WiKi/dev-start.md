# Preparing DEV-environment on Ubuntu-24.04
## VSCode
* download VSCode deb-installer from [official site](https://code.visualstudio.com/download#)
* install:
```bash
sudo apt install ./code_*_amd64.deb
```

## Python
```bash
sudo apt install -y python3 &&
sudo apt install -y python3-venv
sudo apt update
```

## Clang compiler with tools
```bash
wget -qO- https://apt.llvm.org/llvm.sh | sudo bash -s -- 18 &&
sudo apt update &&
sudo apt install -y clang-18 clang-tools-18 build-essential &&
sudo apt install -y cmake ninja
sudo apt update
```

## Gt6 with tools
```bash
sudo apt install -y \
    qt6-base-dev \
    qt6-declarative-dev \
    qt6-base-private-dev \
    libqt6widgets6 \
    libqt6qml6 \
    libqt6quick6 \
    qml6-module-qtquick-controls \
    qml6-module-qtquick-layouts \
    qml6-module-qtquick-window  \
    qml6-module-qtqml-workerscript \
    qml6-module-qtquick-templates &&
sudo apt update
```

## RabbitMQ Server
```bash
sudo apt install rabbitmq-server
sudo apt update
# enable
sudo systemctl start rabbitmq-server
# add autoreload on startup
sudo systemctl enable rabbitmq-server
# check status
sudo rabbitmqctl status
```


## Other tools
```bash
sudo apt install -y \
    libbz2-dev \
    libwayland-dev \
    wayland-protocols \
    zlib1g-dev \
    libfreetype-dev \
    libfontconfig-dev \
    libdbus-1-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev &&
sudo apt update
```
