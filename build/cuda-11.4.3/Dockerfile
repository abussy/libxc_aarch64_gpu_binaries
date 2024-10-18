# CUDA and libxc versions
ARG CUDA_VER=11.4.3

# Use an official NVIDIA CUDA base image
FROM nvidia/cuda:${CUDA_VER}-devel-ubuntu20.04

# Set environment variables for CUDA
#ENV CUDA_VERSION=${cuda_ver}
#ENV NVCC_HOME=/usr/local/cuda/bin

# Set environment variables to suppress prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install essential build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    wget \
    gawk \
    bison \
    zip \
    git \
    software-properties-common \
    pkg-config \
    libssl-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add the PPA for GCC (for example, to install GCC-8)
RUN add-apt-repository ppa:ubuntu-toolchain-r/test && apt-get update

# Install GCC-8 and G++-8
RUN apt-get install -y gcc-8 g++-8

# Update alternatives to set GCC-8 as the default
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 60 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 60

# Verify that the default gcc is the version we installed
RUN gcc --version && g++ --version

# Download and compile glibc 2.28, insures that all GLIBC symbols come from v2.17
WORKDIR /tmp
RUN wget http://ftp.gnu.org/gnu/libc/glibc-2.28.tar.gz \
    && tar -xvf glibc-2.28.tar.gz \
    && cd glibc-2.28 \
    && mkdir build \
    && cd build \
    && ../configure --prefix=/opt/glibc-2.28 \
    && make -j8 \
    && make install

COPY build_script /usr/src/build_script

WORKDIR /usr/src/build_script

RUN bash /usr/src/build_script/build.sh

RUN mv /usr/src/build_script/libxc-7.0.0/libxc_build/products /products
RUN zip -ry /products.zip /products
