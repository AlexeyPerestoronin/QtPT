# Preparing DEV-environment on Ubuntu-24.04
## Python
* sudo apt update
* sudo apt-get update
* sudo apt install -y python3
* sudo apt install -y python3-venv

## Clang
* wget -qO- https://apt.llvm.org/llvm.sh | sudo bash -s -- 18
* sudo apt update
* sudo apt install -y clang-18 clang-tools-18 build-essential

## Cmake
* sudo apt install -y cmake
