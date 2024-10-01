import shutil
import subprocess
import os

cuda_versions = ["11.4.3", "11.5.2", "11.6.1", "11.7.1", "11.8.0", "12.0.0",
                 "12.1.0", "12.2.2", "12.3.2", "12.4.1", "12.5.1", "12.6.1"]

for cuda_ver in cuda_versions:

    #Run the container in the backgroupd for 2 minutes
    command = "docker run -d --rm --platform=linux/arm64 cuda-{}_env sleep 120".format(cuda_ver) 
    container_id = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()

    #Copy over the products.zip archive
    command = "docker cp {}:products.zip .".format(container_id)
    subprocess.call(command, shell=True)

    #Move to binaries directory
    pwd = os.getcwd()
    shutil.move("{}/products.zip".format(pwd), "{}/../binaries/cuda-{}.zip".format(pwd, cuda_ver[:-2]))
    
