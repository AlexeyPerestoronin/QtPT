# Preparing DEV-environment on Ubuntu-24.04
## Python
* sudo apt update
* sudo apt-get update
* sudo apt install -y python3
* sudo apt install -y python3-venv

## Clang compiler with tools
* wget -qO- https://apt.llvm.org/llvm.sh | sudo bash -s -- 18
* sudo apt update
* sudo apt install -y clang-18 clang-tools-18 build-essential
* sudo apt install -y cmake ninja

## Other tools
* sudo apt install -y libbz2-dev libwayland-dev wayland-protocols zlib1g-dev libfreetype-dev libfontconfig-dev libdbus-1-dev libxkbcommon-dev libxkbcommon-x11-dev
* sudo apt install libxkbcommon-dev libxkbcommon-x11-dev

sudo apt install -y qt6-base-dev qt6-declarative-dev qt6-base-private-dev libqt6widgets6 libqt6qml6 libqt6quick6 qml6-module-qtquick-controls qml6-module-qtquick-layouts qml6-module-qtquick-window 
sudo apt update
sudo apt install -y qml6-module-qtqml-workerscript qml6-module-qtquick-templates

sudo apt update



