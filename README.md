This repository contains compiled binaries for the GPU version of the Libxc library, for the `aarch64`
architecture with CUDA. The build recipes are also provided. The binaries can be easily re-generated, 
provided Docker is available on the host machine. These binaries are meant to be redistributes as JLL
packages in Julia, via the BinaryBuilder tool.

The repository is organised as follow:
- src: contains the source code necessary to generate and package the binaries. The `generate_binaries.py`
       script should be run first, followed by `retrieve_binaries.py`.
- build: contains all Docker recipes generated and ran by the above scripts
- binaries: contains the zip archived shared libraries, for each available CUDA version
