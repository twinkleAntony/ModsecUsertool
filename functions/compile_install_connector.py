import configparser
import subprocess
from functions.functions import run_command
import os

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

def compile_and_install_connector():
    SRC_DIR = "/usr/local/src/"
    MODSEC_DIR = "ModSecurity"
    MODSEC_NGINX_DIR = "ModSecurity-nginx"
    NGINX_MODULES_DIR = "/etc/nginx/modules/"

    # Get NGINX version
    nginx_version_output = subprocess.check_output(["nginx", "-v"], text=True, stderr=subprocess.STDOUT)
    nginx_version = nginx_version_output.split("/")[1].split()[0]

    os.chdir(SRC_DIR)
    print(f"Current Working Directory: {os.getcwd()}")

    # Get sources of ModSec nginx connector and nginx

    # Check if ModSecurity-nginx directory already exists
    if os.path.exists(os.path.join(SRC_DIR, MODSEC_NGINX_DIR)):
        print("ModSecurity-nginx repository already exists. Updating...")

        # Change directory to ModSecurity-nginx
        os.chdir(os.path.join(SRC_DIR, MODSEC_NGINX_DIR))

        # Print current working directory after changing
        print(f"Current Working Directory: {os.getcwd()}")

        # Pull the latest changes
        success_pull = run_command(["git", "pull"], shell=False)

        if not success_pull:
            print("Error during Git pull.")
            return
    else:
        # Clone ModSecurity-nginx repository
        success_clone = run_command(["git", "clone", "--depth", "1", f"https://github.com/SpiderLabs/ModSecurity-nginx"], shell=False)

        if not success_clone:
            print("Error during Git clone.")
            return


    os.chdir(SRC_DIR)
    print(f"Current Working Directory: {os.getcwd()}")


    # Download nginx source code
    run_command(["wget", "-O", f"nginx-{nginx_version}.tar.gz", f"http://nginx.org/download/nginx-{nginx_version}.tar.gz"], shell=False)
    run_command(["tar", "zxvf", f"nginx-{nginx_version}.tar.gz"], shell=False)

    # Change directory to nginx source code
    os.chdir(f"nginx-{nginx_version}")
    
    # Configure and compile as a Dynamic Module
    # For 'make modules', it might be necessary to use shell=True due to shell features used by make
    run_command(["./configure", "--with-compat", f"--add-dynamic-module=../ModSecurity-nginx"], shell=False)
    run_command(["make", "modules"], shell=True)  # This might need shell=True

    # Create the modules directory if it doesn't exist
    if not os.path.exists(NGINX_MODULES_DIR):
        os.makedirs(NGINX_MODULES_DIR)

    # Copy the dynamic modsec module to /etc/nginx/modules/
    run_command(["cp", "objs/ngx_http_modsecurity_module.so", "/etc/nginx/modules/"], shell=False)
    run_command(["chmod", "0644", "/etc/nginx/modules/ngx_http_modsecurity_module.so"], shell=False)

