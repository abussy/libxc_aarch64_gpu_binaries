#!/bin/bash

version="7.0.0"
url="https://gitlab.com/libxc/libxc/-/archive/${version}/libxc-${version}.tar.gz"
expected_shasum="8d4e343041c9cd869833822f57744872076ae709a613c118d70605539fb13a77"

wget $url

computed_shasum=$(sha256sum "libxc-${version}.tar.gz" | awk '{print $1}')
if [ ${expected_shasum} != ${computed_shasum} ]; then
    echo "Incorrect sha256sum"
    exit 1
fi

tar --extract --file libxc-${version}.tar.gz
cd libxc-${version}

patch -p1 < ../patches/cmake-cuda.patch
patch -p1 < ../patches/source-fixes.patch

mkdir libxc_build
cd libxc_build

cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_XHOST=OFF -DBUILD_SHARED_LIBS=ON \
      -DENABLE_CUDA=ON -DCMAKE_CUDA_COMPILER=nvcc \
      -DBUILD_TESTING=OFF -DENABLE_FORTRAN=OFF \
      -DCMAKE_INSTALL_PREFIX="$(pwd)/products" \
      -DCMAKE_C_FLAGS="-I/opt/glibc-2.28/include" \
      -DCMAKE_EXE_LINKER_FLAGS="-L/opt/glibc-2.28/lib -Wl,--rpath=/opt/glibc-2.28/lib" \
      -DCMAKE_CUDA_FLAGS="-I/opt/glibc-2.28/include -L/opt/glibc-2.28/lib" \
      -DCMAKE_SHARED_LINKER_FLAGS="-Wl,--disable-new-dtags" \
      -DCMAKE_SKIP_RPATH=OFF \
      -DDISABLE_KXC=ON ..

make -j 4
make install
