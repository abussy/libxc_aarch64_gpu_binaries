import shutil
import subprocess
import os

cuda_versions = ["11.4.3", "11.5.2", "11.6.1", "11.7.1", "11.8.0", "12.0.0",
                 "12.1.0", "12.2.2", "12.3.2", "12.4.1", "12.5.1", "12.6.1"]

for cuda_ver in cuda_versions:

    pwd = os.getcwd()
    if not "cuda-{}".format(cuda_ver) in os.listdir("{}/../build".format(pwd)):
        os.mkdir("{}/../build/cuda-{}".format(pwd, cuda_ver))  

    subprocess.call("cp -r docker_recipe/* ../build/cuda-{}/".format(cuda_ver), shell=True)

    subprocess.call("sed -i 's/insert_version/{}/g' ../build/cuda-{}/Dockerfile".format(cuda_ver, cuda_ver), shell=True)

    #Enable docker cross-platform
    subprocess.call("docker run --rm --privileged multiarch/qemu-user-static --reset -p yes", shell=True)

    #Build docker image
    subprocess.call("docker build -t cuda-{}_env --build-arg CUDA_VER='{}' --platform=linux/arm64 .".format(
                    cuda_ver, cuda_ver), cwd="{}/../build/cuda-{}".format(pwd, cuda_ver), shell=True)
